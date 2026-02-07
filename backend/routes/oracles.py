"""Oracle routes"""

import logging
from flask import Blueprint, request, jsonify
from services.oracle_service import OracleService
from services.ai_service import AIService
from services.reputation_service import ReputationService
from services.evidence_service import EvidenceService
from utils.supabase_client import get_supabase_client
from models.user import User
from models.market import Market

logger = logging.getLogger(__name__)
oracles_bp = Blueprint('oracles', __name__)
oracle_service = OracleService()
ai_service = AIService()
reputation_service = ReputationService()
evidence_service = EvidenceService()

@oracles_bp.route('/predict/<market_id>', methods=['GET', 'POST'])
def get_prediction(market_id):
    """Get oracle prediction for a market"""
    try:
        user_query = None
        if request.method == 'POST':
            data = request.get_json()
            user_query = data.get('query')
        else:
            user_query = request.args.get('query')
        
        prediction, error = oracle_service.get_oracle_prediction(market_id, user_query)
        
        if error:
            return jsonify({'error': error}), 500
        
        return jsonify({'prediction': prediction}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/predict/batch', methods=['POST'])
def get_batch_predictions():
    """Get predictions for multiple markets"""
    try:
        data = request.get_json()
        market_ids = data.get('market_ids', [])
        user_query = data.get('query')
        
        if not market_ids:
            return jsonify({'error': 'market_ids array is required'}), 400
        
        predictions, errors = oracle_service.get_multiple_predictions(market_ids, user_query)
        
        response = {'predictions': predictions}
        if errors:
            response['errors'] = errors
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/submit', methods=['POST'])
def submit_report():
    """
    Submit an oracle report for a market (FR-5.1)
    Users can submit evidence-based truth reports
    """
    try:
        data = request.get_json()
        oracle_id = data.get('oracle_id')  # User ID submitting the report
        market_id = data.get('market_id')
        verdict = data.get('verdict')  # 'true' or 'false'
        evidence = data.get('evidence', [])  # List of URLs or text evidence
        stake = float(data.get('stake', 0))  # Optional stake for oracle reputation
        
        # Validate inputs
        if not oracle_id or not market_id or not verdict:
            return jsonify({'error': 'oracle_id, market_id, and verdict are required'}), 400
        
        if verdict not in ['true', 'false']:
            return jsonify({'error': "verdict must be 'true' or 'false'"}), 400
        
        if not isinstance(evidence, list):
            return jsonify({'error': 'evidence must be a list'}), 400
        
        supabase = get_supabase_client()
        
        # Validate market exists and is active
        market_response = supabase.table('markets').select('*').eq('id', market_id).execute()
        if not market_response.data:
            return jsonify({'error': 'Market not found'}), 404
        
        market = Market.from_dict(market_response.data[0])
        if not market.is_active():
            return jsonify({'error': f'Market is not active (status: {market.status})'}), 400
        
        # Validate user exists
        user_response = supabase.table('users').select('*').eq('id', oracle_id).execute()
        if not user_response.data:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if oracle already submitted a report for this market
        existing_report = supabase.table('oracle_reports').select('*').eq('oracle_id', oracle_id).eq('market_id', market_id).execute()
        if existing_report.data:
            return jsonify({'error': 'You have already submitted a report for this market'}), 400
        
        # Generate AI summary of evidence if available (FR-5.2)
        ai_summary = None
        if evidence:
            try:
                # Use evidence service to fetch and analyze URLs
                evidence_result = evidence_service.extract_evidence_from_urls(evidence, market.text)
                if evidence_result.get('success'):
                    ai_summary = evidence_result.get('ai_summary', '')
                else:
                    # Fallback to simple AI summarization
                    ai_summary = ai_service.summarize_evidence(evidence, market.text)
            except Exception as e:
                logger.warning(f"Failed to generate AI summary: {str(e)}")
                # Fallback
                try:
                    ai_summary = ai_service.summarize_evidence(evidence, market.text)
                except:
                    pass
        
        # Create oracle report
        report_data = {
            'oracle_id': oracle_id,
            'market_id': market_id,
            'verdict': verdict,
            'evidence': evidence,
            'stake': stake,
            'ai_summary': ai_summary,
            'status': 'pending'
        }
        
        report_response = supabase.table('oracle_reports').insert(report_data).execute()
        
        if not report_response.data:
            return jsonify({'error': 'Failed to create oracle report'}), 500
        
        # Check if consensus threshold is reached
        consensus_result = oracle_service.check_consensus(market_id)
        
        response_data = {
            'report': report_response.data[0],
            'consensus': consensus_result
        }
        
        # If consensus reached, automatically resolve market
        if consensus_result.get('consensus_reached'):
            try:
                settlement = oracle_service.settle_market(market_id, consensus_result['outcome'])
                response_data['settlement'] = settlement
            except Exception as e:
                logger.error(f"Failed to auto-settle market after consensus: {str(e)}")
                response_data['settlement_error'] = str(e)
        
        return jsonify(response_data), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error in submit_report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/reports/<market_id>', methods=['GET'])
def get_reports(market_id):
    """Get all oracle reports for a market"""
    try:
        supabase = get_supabase_client()
        
        # Validate market exists
        market_response = supabase.table('markets').select('id').eq('id', market_id).execute()
        if not market_response.data:
            return jsonify({'error': 'Market not found'}), 404
        
        # Get reports with oracle info
        reports_response = supabase.table('oracle_reports').select('*, users!oracle_id(pseudonym)').eq('market_id', market_id).order('created_at', desc=True).execute()
        
        reports = reports_response.data if reports_response.data else []
        
        # Calculate consensus status
        consensus_result = oracle_service.check_consensus(market_id)
        
        return jsonify({
            'reports': reports,
            'consensus': consensus_result
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_reports: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/resolve', methods=['POST'])
def resolve_market():
    """
    Resolve a market through oracle consensus (FR-5.4)
    Can be called manually or automatically when consensus is reached
    """
    try:
        data = request.get_json()
        market_id = data.get('market_id')
        outcome = data.get('outcome')  # Optional: if provided, force resolution
        
        if not market_id:
            return jsonify({'error': 'market_id is required'}), 400
        
        supabase = get_supabase_client()
        
        # Get market
        market_response = supabase.table('markets').select('*').eq('id', market_id).execute()
        if not market_response.data:
            return jsonify({'error': 'Market not found'}), 404
        
        market = Market.from_dict(market_response.data[0])
        
        if not market.is_active():
            return jsonify({'error': f'Market is not active (status: {market.status})'}), 400
        
        # If outcome provided, use it; otherwise check consensus
        if outcome:
            if outcome not in ['true', 'false']:
                return jsonify({'error': "outcome must be 'true' or 'false'"}), 400
            final_outcome = outcome
        else:
            # Check consensus
            consensus_result = oracle_service.check_consensus(market_id)
            if not consensus_result.get('consensus_reached'):
                return jsonify({
                    'error': 'Consensus not reached',
                    'consensus': consensus_result
                }), 400
            final_outcome = consensus_result['outcome']
        
        # Settle the market
        settlement = oracle_service.settle_market(market_id, final_outcome)
        
        return jsonify({
            'message': 'Market resolved successfully',
            'outcome': final_outcome,
            'settlement': settlement
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error in resolve_market: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/reputation/<oracle_id>', methods=['GET'])
def get_oracle_reputation(oracle_id):
    """
    Get oracle reputation statistics (FR-5.5)
    """
    try:
        stats = reputation_service.get_oracle_stats(oracle_id)
        
        if 'error' in stats:
            return jsonify(stats), 404
        
        return jsonify({'oracle': stats}), 200
        
    except Exception as e:
        logger.error(f"Error in get_oracle_reputation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/reputation/top', methods=['GET'])
def get_top_oracles():
    """
    Get top oracles by reputation
    """
    try:
        limit = int(request.args.get('limit', 20))
        
        supabase = get_supabase_client()
        
        # Get top oracles by reputation
        response = supabase.table('users').select('id, pseudonym, oracle_reputation, oracle_reports_count, oracle_correct_count').not_.is_('oracle_reputation', 'null').order('oracle_reputation', desc=True).limit(limit).execute()
        
        if not response.data:
            return jsonify({'oracles': []}), 200
        
        oracles = []
        for rank, user_data in enumerate(response.data, 1):
            reports_count = user_data.get('oracle_reports_count', 0) or 0
            correct_count = user_data.get('oracle_correct_count', 0) or 0
            accuracy = round(correct_count / reports_count * 100, 2) if reports_count > 0 else 0.0
            
            oracles.append({
                'rank': rank,
                'oracle_id': user_data.get('id'),
                'pseudonym': user_data.get('pseudonym', '')[:8] if user_data.get('pseudonym') else '',
                'reputation': round(float(user_data.get('oracle_reputation', 50.0)), 2),
                'total_reports': reports_count,
                'correct_count': correct_count,
                'accuracy': accuracy
            })
        
        return jsonify({'oracles': oracles}), 200
        
    except Exception as e:
        logger.error(f"Error in get_top_oracles: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/evidence/fetch', methods=['POST'])
def fetch_evidence():
    """
    Automatically fetch evidence from URLs (FR-5.2)
    Supports automated oracle bots for public data
    """
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        rumor_text = data.get('rumor_text', '')
        market_id = data.get('market_id')
        
        if not urls or not isinstance(urls, list):
            return jsonify({'error': 'urls array is required'}), 400
        
        # If market_id provided, get market text
        if market_id and not rumor_text:
            supabase = get_supabase_client()
            market_response = supabase.table('markets').select('text').eq('id', market_id).execute()
            if market_response.data:
                rumor_text = market_response.data[0].get('text', '')
        
        # Fetch and analyze evidence
        result = evidence_service.extract_evidence_from_urls(urls, rumor_text)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in fetch_evidence: {str(e)}")
        return jsonify({'error': str(e)}), 500

@oracles_bp.route('/evidence/auto/<market_id>', methods=['POST'])
def auto_fetch_evidence(market_id):
    """
    Automatically fetch evidence for a market (for automated bots) (FR-5.2)
    """
    try:
        supabase = get_supabase_client()
        
        # Get market
        market_response = supabase.table('markets').select('*').eq('id', market_id).execute()
        if not market_response.data:
            return jsonify({'error': 'Market not found'}), 404
        
        market = Market.from_dict(market_response.data[0])
        
        # Auto-fetch evidence
        result = evidence_service.auto_fetch_evidence(market_id, market.text)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in auto_fetch_evidence: {str(e)}")
        return jsonify({'error': str(e)}), 500

