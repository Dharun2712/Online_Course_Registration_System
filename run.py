"""
Flask application entry point
Run with: python run.py
"""
import os
from app import create_app

# Get configuration from environment (default: development)
config_name = os.getenv('FLASK_ENV', 'development')
config_name = config_name.lower()
if config_name not in {'development', 'production', 'testing'}:
    config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', '3000'))
    debug = os.getenv('FLASK_DEBUG', str(app.config['DEBUG'])).lower() in {'1', 'true', 'yes', 'on'}
    print("Starting CourseHub Platform...")
    print(f"Listening on 0.0.0.0:{port}")
    print(f"⚙️  Environment: {config_name}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
