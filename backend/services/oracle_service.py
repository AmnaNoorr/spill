"""Oracle service for market oracle operations"""

import logging
from datetime import datetime
from typing import Dict, List
from services.ai_service import AIService
from services.market_service import MarketService
from services.reputation_service import ReputationService
from utils.supabase_client import get_supabase_client
from models.market import Market
from models.user import User
from models.position import Position
import numpy as np

logger = logging.getLogger(__name__)

class OracleService:
    """Service for oracle operations"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.market_service = MarketService()
        self.reputation_service = ReputationService()
    
    def get_oracle_prediction(self, market_id, user_query=None):
        """Get oracle prediction for a market"""
        # Get market data
        market, error = self.market_service.get_market_by_id(market_id)
        if error:
            return None, error
        
        # Get AI prediction
        market_data = market.to_dict()
        prediction, error = self.ai_service.generate_prediction(market_data, user_query)
        if error:
            return None, error
        
        # Calculate confidence score (simplified)
        confidence = self._calculate_confidence(market_data, prediction)
        
        return {
            'market_id': market_id,
            'prediction': prediction,
            'confidence': confidence,
            'timestamp': market.updated_at if hasattr(market, 'updated_at') else None
        }, None
    
    def _calculate_confidence(self, market_data, prediction):
        """Calculate confidence score for prediction"""
        # Simplified confidence calculation
        # In production, this would use more sophisticated methods
        base_confidence = 0.5
        
        # Adjust based on market data availability
        if market_data.get('status') == 'active':
            base_confidence += 0.2
        
        # Add some randomness for demo (replace with actual ML model)
        noise = np.random.normal(0, 0.1)
        confidence = np.clip(base_confidence + noise, 0.0, 1.0)
        
        return float(confidence)
    
    def get_multiple_predictions(self, market_ids, user_query=None):
        """Get predictions for multiple markets"""
        predictions = []
        errors = []
        
        for market_id in market_ids:
            prediction, error = self.get_oracle_prediction(market_id, user_query)
            if error:
                errors.append(f"Market {market_id}: {error}")
            else:
                predictions.append(prediction)
        
        return predictions, errors if errors else None
    
    def check_consensus(self, market_id: str, threshold: float = 0.6) -> Dict:
        """
        Check if oracle consensus threshold is reached for a market (FR-5.3)
        
        Args:
            market_id: Market ID to check
            threshold: Consensus threshold (default 0.6 = 60% agreement)
        
        Returns:
            Dictionary with consensus_reached, outcome, true_votes, false_votes, total_votes, percentage
        """
        try:
            supabase = get_supabase_client()
            
            # Get all pending/accepted reports for this market
            reports_response = supabase.table('oracle_reports').select('*').eq('market_id', market_id).in_('status', ['pending', 'accepted']).execute()
            
            if not reports_response.data:
                return {
                    'consensus_reached': False,
                    'outcome': None,
                    'true_votes': 0,
                    'false_votes': 0,
                    'total_votes': 0,
                    'percentage': 0.0,
                    'threshold': threshold
                }
            
            reports = reports_response.data
            total_votes = len(reports)
            
            # Count votes by verdict
            true_votes = sum(1 for r in reports if r.get('verdict') == 'true')
            false_votes = sum(1 for r in reports if r.get('verdict') == 'false')
            
            # Calculate percentages
            true_percentage = true_votes / total_votes if total_votes > 0 else 0.0
            false_percentage = false_votes / total_votes if total_votes > 0 else 0.0
            
            # Weight reports by reputation (FR-5.5)
            weighted_consensus = self.reputation_service.weight_report_by_reputation(reports)
            weighted_true_pct = weighted_consensus.get('weighted_true_percentage', 0.0)
            weighted_false_pct = weighted_consensus.get('weighted_false_percentage', 0.0)
            
            # Check if consensus reached (either true or false exceeds threshold)
            # Use both simple majority and weighted consensus
            consensus_reached = False
            outcome = None
            
            # Simple majority check
            if true_percentage >= threshold:
                consensus_reached = True
                outcome = 'true'
            elif false_percentage >= threshold:
                consensus_reached = True
                outcome = 'false'
            
            # Weighted consensus check (if simple doesn't reach threshold)
            if not consensus_reached:
                if weighted_true_pct >= threshold * 100:
                    consensus_reached = True
                    outcome = 'true'
                elif weighted_false_pct >= threshold * 100:
                    consensus_reached = True
                    outcome = 'false'
            
            return {
                'consensus_reached': consensus_reached,
                'outcome': outcome,
                'true_votes': true_votes,
                'false_votes': false_votes,
                'total_votes': total_votes,
                'true_percentage': round(true_percentage, 2),
                'false_percentage': round(false_percentage, 2),
                'weighted_true_percentage': weighted_true_pct,
                'weighted_false_percentage': weighted_false_pct,
                'threshold': threshold
            }
            
        except Exception as e:
            logger.error(f"Error in check_consensus: {str(e)}")
            return {
                'consensus_reached': False,
                'outcome': None,
                'error': str(e)
            }
    
    def settle_market(self, market_id: str, outcome: str) -> Dict:
        """
        Settle a market and distribute payouts
        
        Args:
            market_id: Market ID to settle
            outcome: 'true' or 'false'
        
        Returns:
            Dictionary with payouts, winners, losers, and total_paid
        
        Raises:
            ValueError: If market is not active or outcome is invalid
            Exception: For database errors
        """
        if outcome not in ['true', 'false']:
            raise ValueError("Outcome must be 'true' or 'false'")
        
        supabase = get_supabase_client()
        
        try:
            # 1. Get market from Supabase
            market_response = supabase.table('markets').select('*').eq('id', market_id).execute()
            if not market_response.data:
                raise ValueError(f"Market {market_id} not found")
            
            market = Market.from_dict(market_response.data[0])
            
            # 2. Validate active
            if not market.is_active():
                raise ValueError(f"Market {market_id} is not active (status: {market.status})")
            
            # 3. Get all active positions
            positions_response = supabase.table('positions').select('*').eq('market_id', market_id).eq('status', 'open').execute()
            positions = [Position.from_dict(p) for p in positions_response.data] if positions_response.data else []
            
            # 4. Calculate submitter payout: stake*2 if TRUE else 0
            submitter_payout = 0.0
            if market.submitter_id:
                if outcome == 'true':
                    submitter_payout = market.stake * 2
                else:
                    submitter_payout = 0.0
            
            # 5. Calculate payouts for each position
            payouts = {}
            winners = []
            losers = []
            
            # Process submitter payout
            if submitter_payout > 0 and market.submitter_id:
                payouts[market.submitter_id] = payouts.get(market.submitter_id, 0.0) + submitter_payout
                winners.append(market.submitter_id)
            
            # Process positions
            for position in positions:
                user_id = position.user_id
                
                if position.type == 'true':  # Long position
                    payout = position.calculate_payout_if_true() if outcome == 'true' else 0.0
                else:  # Short position (false)
                    payout = position.calculate_payout_if_false() if outcome == 'false' else 0.0
                
                if payout > 0:
                    payouts[user_id] = payouts.get(user_id, 0.0) + payout
                    winners.append(user_id)
                else:
                    if user_id not in winners:
                        losers.append(user_id)
            
            # 6. Update all user balances
            user_updates = {}
            for user_id, payout_amount in payouts.items():
                # Get user
                user_response = supabase.table('users').select('*').eq('id', user_id).execute()
                if not user_response.data:
                    logger.warning(f"User {user_id} not found for payout")
                    continue
                
                user = User.from_dict(user_response.data[0])
                
                # Calculate locked CC for this market (sum of all positions)
                user_positions = [p for p in positions if p.user_id == user_id]
                total_locked = sum(p.collateral for p in user_positions)
                
                # Unlock locked CC for this market
                user.unlock_balance(total_locked)
                
                # Add payout to available
                user.available_balance += payout_amount
                
                # Update total_earned
                user.total_earned += payout_amount
                
                user_updates[user_id] = {
                    'available_balance': user.available_balance,
                    'locked_balance': user.locked_balance,
                    'total_earned': user.total_earned
                }
            
            # Handle submitter if outcome is false (unlock their stake)
            if outcome == 'false' and market.submitter_id and market.submitter_id not in payouts:
                submitter_response = supabase.table('users').select('*').eq('id', market.submitter_id).execute()
                if submitter_response.data:
                    submitter = User.from_dict(submitter_response.data[0])
                    # Unlock the submitter's stake (stake was locked when market was created)
                    try:
                        submitter.unlock_balance(market.stake)
                        user_updates[market.submitter_id] = {
                            'available_balance': submitter.available_balance,
                            'locked_balance': submitter.locked_balance
                        }
                    except ValueError:
                        # Stake might already be unlocked or amount mismatch
                        logger.warning(f"Could not unlock stake for submitter {market.submitter_id}")
            
            # Update losers (unlock their locked balance, record loss)
            for user_id in losers:
                if user_id in payouts:
                    continue  # Already processed
                
                user_response = supabase.table('users').select('*').eq('id', user_id).execute()
                if not user_response.data:
                    continue
                
                user = User.from_dict(user_response.data[0])
                user_positions = [p for p in positions if p.user_id == user_id]
                total_locked = sum(p.collateral for p in user_positions)
                total_cost = sum(p.cost_basis for p in user_positions)
                
                # Unlock locked CC
                try:
                    user.unlock_balance(total_locked)
                except ValueError:
                    logger.warning(f"Could not unlock balance for user {user_id}")
                
                # Record loss
                user.deduct_loss(total_cost)
                
                user_updates[user_id] = {
                    'available_balance': user.available_balance,
                    'locked_balance': user.locked_balance,
                    'total_lost': user.total_lost
                }
            
            # Apply all user updates
            for user_id, update_data in user_updates.items():
                supabase.table('users').update(update_data).eq('id', user_id).execute()
            
            # 7. Close all positions
            for position in positions:
                supabase.table('positions').update({
                    'status': 'closed'
                }).eq('id', position.id).execute()
            
            # 8. Update oracle reports and reputation (FR-5.5)
            oracle_reports_response = supabase.table('oracle_reports').select('*').eq('market_id', market_id).execute()
            if oracle_reports_response.data:
                for report in oracle_reports_response.data:
                    oracle_id = report.get('oracle_id')
                    report_verdict = report.get('verdict')
                    was_correct = (report_verdict == outcome)
                    
                    # Update report with correctness
                    supabase.table('oracle_reports').update({
                        'was_correct': was_correct,
                        'status': 'accepted'
                    }).eq('id', report.get('id')).execute()
                    
                    # Update oracle reputation
                    reputation_update = self.reputation_service.update_oracle_reputation(oracle_id, was_correct)
                    if 'error' not in reputation_update:
                        # Store reputation awarded in report
                        reputation_change = reputation_update.get('reputation_change', 0.0)
                        supabase.table('oracle_reports').update({
                            'reputation_awarded': reputation_change
                        }).eq('id', report.get('id')).execute()
            
            # 9. Update market
            resolved_status = 'resolved_true' if outcome == 'true' else 'resolved_false'
            supabase.table('markets').update({
                'status': resolved_status,
                'resolved_at': datetime.utcnow().isoformat()
            }).eq('id', market_id).execute()
            
            # Calculate total paid
            total_paid = sum(payouts.values())
            
            return {
                'payouts': payouts,
                'winners': list(set(winners)),
                'losers': list(set(losers)),
                'total_paid': total_paid
            }
            
        except Exception as e:
            logger.error(f"Error settling market {market_id}: {str(e)}")
            raise

