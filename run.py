"""
Flask application entry point
Run with: python run.py
"""
import os
from app import create_app

# Get configuration from environment (default: development)
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    print("🚀 Starting CourseHub Platform...")
    print(f"📍 Access the application at: http://localhost:3000")
    print(f"⚙️  Environment: {config_name}")
    
    app.run(
        host='0.0.0.0',
        port=3000,
        debug=True
    )
