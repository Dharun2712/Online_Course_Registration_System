"""
Password Hashing Utilities
Uses Werkzeug's security functions
"""
from werkzeug.security import generate_password_hash as _generate_hash
from werkzeug.security import check_password_hash as _check_hash

def hash_password(password):
    """
    Hash a password for storing
    Args:
        password: Plain text password
    Returns:
        Hashed password string
    """
    return _generate_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(password, hashed_password):
    """
    Verify a password against a hash
    Args:
        password: Plain text password to verify
        hashed_password: Hashed password to compare against
    Returns:
        Boolean - True if password matches
    """
    return _check_hash(hashed_password, password)

def is_strong_password(password):
    """
    Check if password meets strength requirements
    Requirements:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains digit
    Args:
        password: Password to check
    Returns:
        Tuple (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"
