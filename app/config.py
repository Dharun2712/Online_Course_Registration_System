import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MONGO_URI = os.getenv('MONGO_URI')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'online_course_platform')
    
    # JWT Configuration
    JWT_EXPIRATION_HOURS = 24
    
    # Application settings
    DEBUG = True
    TESTING = False
    
    # Pagination
    COURSES_PER_PAGE = 12
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'mp3', 'doc', 'docx', 'ppt', 'pptx'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

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
