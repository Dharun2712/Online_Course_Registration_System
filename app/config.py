import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MONGO_URI = os.getenv('MONGO_URI') or os.getenv('CUSTOMCONNSTR_MONGO_URI')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    DATABASE_NAME = os.getenv('MONGO_DB_NAME') or os.getenv('DATABASE_NAME', 'online_course_platform')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '')
    
    # JWT Configuration
    JWT_EXPIRATION_HOURS = 24
    
    # Application settings
    DEBUG = os.getenv('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes', 'on'}
    TESTING = False
    
    # Pagination
    COURSES_PER_PAGE = 12
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'mp3', 'doc', 'docx', 'ppt', 'pptx'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() in {'1', 'true', 'yes', 'on'}

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
