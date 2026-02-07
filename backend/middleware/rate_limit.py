"""Rate limiting middleware (NFR-4)"""

import time
from functools import wraps
from flask import request, jsonify
from collections import defaultdict

# In-memory rate limit store (use Redis in production)
_rate_limit_store = defaultdict(list)

def rate_limit(max_requests=20, window_seconds=60):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
    
    Usage:
        @rate_limit(max_requests=20, window_seconds=60)
        def my_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier (use IP address or user_id if available)
            client_id = request.remote_addr
            if request.is_json and request.get_json():
                user_id = request.get_json().get('user_id')
                if user_id:
                    client_id = f"{client_id}:{user_id}"
            
            # Clean old entries
            current_time = time.time()
            _rate_limit_store[client_id] = [
                timestamp for timestamp in _rate_limit_store[client_id]
                if current_time - timestamp < window_seconds
            ]
            
            # Check rate limit
            if len(_rate_limit_store[client_id]) >= max_requests:
                return jsonify({
                    'error': f'Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.'
                }), 429
            
            # Record this request
            _rate_limit_store[client_id].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


