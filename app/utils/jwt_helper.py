"""
JWT Helper - Token generation and validation
"""
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
ALGORITHM = 'HS256'
EXPIRATION_HOURS = 24

def generate_token(user_data):
    """
    Generate JWT token for authenticated user
    Args:
        user_data: Dictionary containing user info (id, email, role)
    Returns:
        JWT token string
    """
    payload = {
        'user_id': str(user_data.get('_id') or user_data.get('id')),
        'email': user_data.get('email'),
        'role': user_data.get('role'),
        'name': user_data.get('name'),
        'exp': datetime.utcnow() + timedelta(hours=EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    """
    Decode and validate JWT token
    Args:
        token: JWT token string
    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def get_token_from_request():
    """Extract token from Authorization header"""
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Bearer '):
        return auth_header.replace('Bearer ', '')
    
    return None

def token_required(f):
    """
    Decorator to protect routes that require authentication
    Usage: @token_required
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_request()
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = decode_token(token)
        
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Add user info to request context
        request.current_user = payload
        
        return f(*args, **kwargs)
    
    return decorated

def role_required(required_role):
    """
    Decorator to protect routes that require specific role
    Usage: @role_required('admin')
    Args:
        required_role: Required user role (student/instructor/admin)
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_from_request()
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            payload = decode_token(token)
            
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            if payload.get('role') != required_role:
                return jsonify({'error': f'Unauthorized. {required_role.capitalize()} role required'}), 403
            
            # Add user info to request context
            request.current_user = payload
            
            return f(*args, **kwargs)
        
        return decorated
    
    return decorator

def roles_required(*required_roles):
    """
    Decorator to protect routes that require one of multiple roles
    Usage: @roles_required('instructor', 'admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_from_request()
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            payload = decode_token(token)
            
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            if payload.get('role') not in required_roles:
                roles_str = ', '.join(required_roles)
                return jsonify({'error': f'Unauthorized. One of these roles required: {roles_str}'}), 403
            
            # Add user info to request context
            request.current_user = payload
            
            return f(*args, **kwargs)
        
        return decorated
    
    return decorator

def get_current_user():
    """Get current authenticated user from request context"""
    return getattr(request, 'current_user', None)
