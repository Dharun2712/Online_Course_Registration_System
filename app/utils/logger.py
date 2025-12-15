"""
Logger Utility
Simple logging configuration for the application
"""
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()  # Also print to console
    ]
)

def get_logger(name):
    """
    Get a logger instance
    Args:
        name: Name of the logger (usually __name__)
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Application loggers
app_logger = get_logger('app')
auth_logger = get_logger('auth')
db_logger = get_logger('database')
api_logger = get_logger('api')

def log_api_request(method, endpoint, user_id=None, status=None):
    """Log API request"""
    api_logger.info(f"{method} {endpoint} | User: {user_id} | Status: {status}")

def log_auth_attempt(email, success, ip=None):
    """Log authentication attempt"""
    status = "SUCCESS" if success else "FAILED"
    auth_logger.info(f"Login attempt: {email} | {status} | IP: {ip}")

def log_db_operation(operation, collection, success):
    """Log database operation"""
    status = "SUCCESS" if success else "FAILED"
    db_logger.info(f"DB {operation}: {collection} | {status}")

def log_error(error, context=""):
    """Log error with context"""
    app_logger.error(f"Error in {context}: {str(error)}")

def log_info(message):
    """Log informational message"""
    app_logger.info(message)

def log_warning(message):
    """Log warning message"""
    app_logger.warning(message)
