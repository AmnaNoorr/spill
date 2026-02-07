"""Oracle reputation tracking service (FR-5.5)"""

import logging
from typing import Dict
from utils.supabase_client import get_supabase_client
from models.user import User

logger = logging.getLogger(__name__)

class ReputationService:
    """Service for tracking and updating oracle reputation"""
    
    @staticmethod
    def calculate_reputation(correct_count: int, total_count: int) -> float:
        """
        Calculate reputation score based on accuracy
        
        Args:
            correct_count: Number of correct reports
            total_count: Total number of reports
        
        Returns:
            Reputation score (0-100)
        """
        if total_count == 0:
            return 50.0  # Default starting reputation
        
        accuracy = correct_count / total_count
        # Scale to 0-100, with 50% accuracy = 50 reputation
        reputation = accuracy * 100.0
        return max(0.0, min(100.0, reputation))
    
    @staticmethod
    def update_oracle_reputation(oracle_id: str, was_correct: bool) -> Dict:
        """
        Update oracle reputation after market resolution
        
        Args:
            oracle_id: Oracle user ID
            was_correct: Whether the oracle's report was correct
        
        Returns:
            Dictionary with updated reputation info
        """
        try:
            supabase = get_supabase_client()
            
            # Get current user data
            user_response = supabase.table('users').select('*').eq('id', oracle_id).execute()
            if not user_response.data:
                return {'error': 'User not found'}
            
            user = User.from_dict(user_response.data[0])
            
            # Get current reputation fields (with defaults)
            reports_count = getattr(user, 'oracle_reports_count', 0) or 0
            correct_count = getattr(user, 'oracle_correct_count', 0) or 0
            incorrect_count = getattr(user, 'oracle_incorrect_count', 0) or 0
            current_reputation = getattr(user, 'oracle_reputation', 50.0) or 50.0
            
            # Update counts
            reports_count += 1
            if was_correct:
                correct_count += 1
                # Award reputation bonus for correct reports
                reputation_bonus = 2.0  # +2 points per correct report
            else:
                incorrect_count += 1
                # Penalty for incorrect reports
                reputation_bonus = -1.0  # -1 point per incorrect report
            
            # Calculate new reputation
            new_reputation = ReputationService.calculate_reputation(correct_count, reports_count)
            # Apply bonus/penalty
            new_reputation = max(0.0, min(100.0, new_reputation + reputation_bonus))
            
            # Update user in database
            update_data = {
                'oracle_reputation': new_reputation,
                'oracle_reports_count': reports_count,
                'oracle_correct_count': correct_count,
                'oracle_incorrect_count': incorrect_count
            }
            
            supabase.table('users').update(update_data).eq('id', oracle_id).execute()
            
            return {
                'oracle_id': oracle_id,
                'old_reputation': current_reputation,
                'new_reputation': new_reputation,
                'reputation_change': new_reputation - current_reputation,
                'total_reports': reports_count,
                'correct_count': correct_count,
                'incorrect_count': incorrect_count,
                'accuracy': round(correct_count / reports_count * 100, 2) if reports_count > 0 else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error updating oracle reputation: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def get_oracle_stats(oracle_id: str) -> Dict:
        """
        Get oracle statistics
        
        Args:
            oracle_id: Oracle user ID
        
        Returns:
            Dictionary with oracle statistics
        """
        try:
            supabase = get_supabase_client()
            
            user_response = supabase.table('users').select('*').eq('id', oracle_id).execute()
            if not user_response.data:
                return {'error': 'User not found'}
            
            user = User.from_dict(user_response.data[0])
            
            reports_count = getattr(user, 'oracle_reports_count', 0) or 0
            correct_count = getattr(user, 'oracle_correct_count', 0) or 0
            incorrect_count = getattr(user, 'oracle_incorrect_count', 0) or 0
            reputation = getattr(user, 'oracle_reputation', 50.0) or 50.0
            
            accuracy = round(correct_count / reports_count * 100, 2) if reports_count > 0 else 0.0
            
            return {
                'oracle_id': oracle_id,
                'reputation': round(reputation, 2),
                'total_reports': reports_count,
                'correct_count': correct_count,
                'incorrect_count': incorrect_count,
                'accuracy': accuracy
            }
            
        except Exception as e:
            logger.error(f"Error getting oracle stats: {str(e)}")
            return {'error': str(e)}
    
    @staticmethod
    def weight_report_by_reputation(reports: list) -> Dict:
        """
        Weight oracle reports by reputation for consensus calculation
        
        Args:
            reports: List of oracle report dictionaries
        
        Returns:
            Dictionary with weighted consensus
        """
        try:
            supabase = get_supabase_client()
            
            if not reports:
                return {
                    'weighted_true': 0.0,
                    'weighted_false': 0.0,
                    'total_weight': 0.0
                }
            
            weighted_true = 0.0
            weighted_false = 0.0
            total_weight = 0.0
            
            for report in reports:
                oracle_id = report.get('oracle_id')
                verdict = report.get('verdict')
                
                # Get oracle reputation
                user_response = supabase.table('users').select('oracle_reputation').eq('id', oracle_id).execute()
                if user_response.data:
                    reputation = float(user_response.data[0].get('oracle_reputation', 50.0))
                else:
                    reputation = 50.0  # Default
                
                # Weight by reputation (reputation / 100)
                weight = reputation / 100.0
                total_weight += weight
                
                if verdict == 'true':
                    weighted_true += weight
                elif verdict == 'false':
                    weighted_false += weight
            
            return {
                'weighted_true': weighted_true,
                'weighted_false': weighted_false,
                'total_weight': total_weight,
                'weighted_true_percentage': round(weighted_true / total_weight * 100, 2) if total_weight > 0 else 0.0,
                'weighted_false_percentage': round(weighted_false / total_weight * 100, 2) if total_weight > 0 else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error weighting reports by reputation: {str(e)}")
            return {
                'weighted_true': 0.0,
                'weighted_false': 0.0,
                'total_weight': 0.0,
                'error': str(e)
            }

