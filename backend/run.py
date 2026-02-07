"""Run script for Flask application"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

# Get configuration
flask_env = os.getenv('FLASK_ENV', 'development')
debug_mode = flask_env == 'development'

# Print startup info
print("="*60)
print("SipNSecret Backend Server")
print("="*60)
print(f"Environment: {flask_env}")
print(f"Debug Mode: {debug_mode}")
print(f"Port: 5000")
print("="*60)

# Print registered routes
print("\nRegistered Routes:")
print("-"*60)
for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
    print(f"{rule.rule:40} {methods:20}")
print("-"*60 + "\n")

# Run the app
if __name__ == '__main__':
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

