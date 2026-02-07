"""Authentication routes"""

import logging
from flask import Blueprint, request, jsonify
from utils.supabase_client import get_supabase_client
from models.user import User

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': {
                    'username': username
                }
            }
        })
        
        if response.user:
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                }
            }), 201
        else:
            return jsonify({'error': 'Registration failed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                },
                'access_token': response.session.access_token if response.session else None
            }), 200
        else:
            return jsonify({'error': 'Login failed'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current authenticated user"""
    try:
        supabase = get_supabase_client()
        user = supabase.auth.get_user()
        
        if user:
            return jsonify({
                'user': {
                    'id': user.user.id,
                    'email': user.user.email
                }
            }), 200
        else:
            return jsonify({'error': 'Not authenticated'}), 401
            
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/initialize', methods=['POST'])
def initialize():
    """Initialize or get existing user"""
    try:
        data = request.get_json()
        pseudonym = data.get('pseudonym')
        
        if not pseudonym:
            return jsonify({'error': 'Pseudonym is required'}), 400
        
        supabase = get_supabase_client()
        
        # Check if user exists by pseudonym
        existing_user = supabase.table('users').select('*').eq('pseudonym', pseudonym).execute()
        
        if existing_user.data:
            # User exists, return it
            user = User.from_dict(existing_user.data[0])
            return jsonify({'user': user.to_dict()}), 200
        else:
            # Create new user with 100 CC
            new_user_data = {
                'pseudonym': pseudonym,
                'available_balance': 100.0,
                'locked_balance': 0.0,
                'total_earned': 0.0,
                'total_lost': 0.0
            }
            
            response = supabase.table('users').insert(new_user_data).execute()
            
            if response.data:
                user = User.from_dict(response.data[0])
                return jsonify({'user': user.to_dict()}), 201
            else:
                return jsonify({'error': 'Failed to create user'}), 500
                
    except Exception as e:
        logger.error(f"Error in initialize: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user with balance, positions count, win rate"""
    try:
        supabase = get_supabase_client()
        
        # Get user
        user_response = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if not user_response.data:
            return jsonify({'error': 'User not found'}), 404
        
        user = User.from_dict(user_response.data[0])
        
        # Get positions count
        positions_response = supabase.table('positions').select('id', count='exact').eq('user_id', user_id).execute()
        positions_count = positions_response.count if hasattr(positions_response, 'count') else len(positions_response.data) if positions_response.data else 0
        
        # Calculate win rate (positions with status='won' / total closed positions)
        closed_positions = supabase.table('positions').select('status').eq('user_id', user_id).in_('status', ['won', 'lost']).execute()
        total_closed = len(closed_positions.data) if closed_positions.data else 0
        won_positions = [p for p in (closed_positions.data or []) if p.get('status') == 'won']
        win_rate = len(won_positions) / total_closed if total_closed > 0 else 0.0
        
        user_dict = user.to_dict()
        user_dict['positions_count'] = positions_count
        user_dict['win_rate'] = round(win_rate, 2)
        
        return jsonify({'user': user_dict}), 200
        
    except Exception as e:
        logger.error(f"Error in get_user: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
def get_users():
    """Get top 20 users by total balance"""
    try:
        supabase = get_supabase_client()
        
        # Get top 20 users by total balance (available + locked)
        # Note: We'll calculate total_balance in the query or after fetching
        response = supabase.table('users').select('id, pseudonym, available_balance, locked_balance, total_earned').order('available_balance', desc=True).limit(20).execute()
        
        if not response.data:
            return jsonify({'users': []}), 200
        
        users_list = []
        for rank, user_data in enumerate(response.data, 1):
            total_balance = user_data.get('available_balance', 0.0) + user_data.get('locked_balance', 0.0)
            users_list.append({
                'rank': rank,
                'pseudonym': user_data.get('pseudonym', '')[:8] if user_data.get('pseudonym') else '',
                'balance': round(total_balance, 2),
                'total_earned': round(user_data.get('total_earned', 0.0), 2)
            })
        
        return jsonify({'users': users_list}), 200
        
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        return jsonify({'error': str(e)}), 500

