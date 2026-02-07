import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.auth import auth_bp
from routes.markets import markets_bp
from routes.oracles import oracles_bp
from utils.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(markets_bp, url_prefix='/markets')
    app.register_blueprint(oracles_bp, url_prefix='/oracles')
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': str(error)}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check with database and AI status"""
        try:
            # Check database connection
            supabase = get_supabase_client()
            supabase.table('users').select('id').limit(1).execute()
            database_status = 'connected'
        except Exception as e:
            logger.warning(f"Database health check failed: {str(e)}")
            database_status = 'disconnected'
        
        # Check AI service
        try:
            from services.ai_service import AIService
            ai_service = AIService()
            ai_status = 'available' if ai_service.client else 'unavailable'
        except Exception as e:
            logger.warning(f"AI service health check failed: {str(e)}")
            ai_status = 'unavailable'
        
        return jsonify({
            'status': 'healthy',
            'database': database_status,
            'ai': ai_status
        }), 200
    
    # Stats endpoint
    @app.route('/stats')
    def stats():
        """Get application statistics"""
        try:
            supabase = get_supabase_client()
            
            # Total users
            users_response = supabase.table('users').select('id', count='exact').execute()
            total_users = users_response.count if hasattr(users_response, 'count') else len(users_response.data) if users_response.data else 0
            
            # Total markets
            markets_response = supabase.table('markets').select('id', count='exact').execute()
            total_markets = markets_response.count if hasattr(markets_response, 'count') else len(markets_response.data) if markets_response.data else 0
            
            # Active markets
            active_markets_response = supabase.table('markets').select('id', count='exact').eq('status', 'active').execute()
            active_markets = active_markets_response.count if hasattr(active_markets_response, 'count') else len(active_markets_response.data) if active_markets_response.data else 0
            
            # Total CC locked (sum of locked_balance from all users)
            users_data = supabase.table('users').select('locked_balance').execute()
            total_cc_locked = sum(float(u.get('locked_balance', 0)) for u in (users_data.data or []))
            
            return jsonify({
                'total_users': total_users,
                'total_markets': total_markets,
                'active_markets': active_markets,
                'total_cc_locked': round(total_cc_locked, 2)
            }), 200
            
        except Exception as e:
            logger.error(f"Error in stats endpoint: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    # Print registered routes (will be printed when app starts via run.py)
    # Routes are printed in run.py on startup
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

