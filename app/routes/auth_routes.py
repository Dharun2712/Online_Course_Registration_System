"""
Authentication Routes
Handles user registration, login, and profile management
"""
from flask import Blueprint, request, jsonify, current_app
from app.services.auth_service import AuthService
from app.utils.jwt_helper import token_required, get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    auth_service = AuthService(current_app.db)
    
    success, message, token = auth_service.register(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role', 'student')
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': message,
            'token': token
        }), 201
    else:
        return jsonify({'success': False, 'error': message}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    auth_service = AuthService(current_app.db)
    
    success, message, token, user = auth_service.login(
        email=data.get('email'),
        password=data.get('password')
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': message,
            'token': token,
            'user': user
        }), 200
    else:
        return jsonify({'success': False, 'error': message}), 401

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    current_user = get_current_user()
    auth_service = AuthService(current_app.db)
    
    user = auth_service.get_user_profile(current_user['user_id'])
    
    if user:
        return jsonify({'success': True, 'user': user}), 200
    else:
        return jsonify({'success': False, 'error': 'User not found'}), 404

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    current_user = get_current_user()
    data = request.get_json()
    
    auth_service = AuthService(current_app.db)
    
    success, message = auth_service.update_profile(current_user['user_id'], data)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """Change user password"""
    current_user = get_current_user()
    data = request.get_json()
    
    auth_service = AuthService(current_app.db)
    
    success, message = auth_service.change_password(
        user_id=current_user['user_id'],
        old_password=data.get('old_password'),
        new_password=data.get('new_password')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token():
    """Verify if token is valid"""
    current_user = get_current_user()
    return jsonify({
        'success': True,
        'valid': True,
        'user': current_user
    }), 200
