"""
Authentication Service
Handles user authentication logic
"""
from app.models.user_model import User
from app.utils.jwt_helper import generate_token
from app.utils.validators import validate_email, validate_required_fields, validate_role
from app.utils.password_hash import is_strong_password
from app.utils.logger import log_auth_attempt, log_error

class AuthService:
    def __init__(self, db):
        self.user_model = User(db)
    
    def register(self, name, email, password, role='student'):
        """
        Register a new user
        Returns: (success, message, token/None)
        """
        # Validate inputs
        is_valid, message = validate_email(email)
        if not is_valid:
            return False, message, None
        
        is_valid, message = validate_role(role)
        if not is_valid:
            return False, message, None
        
        is_valid, message = is_strong_password(password)
        if not is_valid:
            return False, message, None
        
        if not name or len(name) < 2:
            return False, "Name must be at least 2 characters", None
        
        # Create user
        try:
            user_id = self.user_model.create(name, email, password, role)
            
            if not user_id:
                log_auth_attempt(email, False)
                return False, "Email already exists", None
            
            # Get user data and generate token
            user = self.user_model.find_by_id(user_id)
            token = generate_token(user)
            
            log_auth_attempt(email, True)
            return True, "Registration successful", token
        
        except Exception as e:
            log_error(str(e), "auth_service.register")
            return False, "Registration failed", None
    
    def login(self, email, password):
        """
        Authenticate user
        Returns: (success, message, token/None, user_data/None)
        """
        is_valid, message = validate_email(email)
        if not is_valid:
            return False, message, None, None
        
        try:
            user = self.user_model.authenticate(email, password)
            
            if not user:
                log_auth_attempt(email, False)
                return False, "Invalid email or password", None, None
            
            if not user.get('is_active', True):
                return False, "Account is deactivated", None, None
            
            token = generate_token(user)
            log_auth_attempt(email, True)
            
            return True, "Login successful", token, user
        
        except Exception as e:
            log_error(str(e), "auth_service.login")
            return False, "Login failed", None, None
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        is_valid, message = is_strong_password(new_password)
        if not is_valid:
            return False, message
        
        try:
            success = self.user_model.change_password(user_id, old_password, new_password)
            
            if success:
                return True, "Password changed successfully"
            else:
                return False, "Current password is incorrect"
        
        except Exception as e:
            log_error(str(e), "auth_service.change_password")
            return False, "Failed to change password"
    
    def get_user_profile(self, user_id):
        """Get user profile"""
        try:
            user = self.user_model.find_by_id(user_id)
            return user
        except Exception as e:
            log_error(str(e), "auth_service.get_user_profile")
            return None
    
    def update_profile(self, user_id, updates):
        """Update user profile"""
        # Remove sensitive fields that shouldn't be updated this way
        updates.pop('password', None)
        updates.pop('email', None)
        updates.pop('role', None)
        
        try:
            success = self.user_model.update(user_id, updates)
            if success:
                return True, "Profile updated successfully"
            else:
                return False, "Failed to update profile"
        except Exception as e:
            log_error(str(e), "auth_service.update_profile")
            return False, "Failed to update profile"
