"""
Input Validators
"""
import re
from datetime import datetime

def validate_email(email):
    """
    Validate email format
    Returns: Tuple (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    return True, "Email is valid"

def validate_required_fields(data, required_fields):
    """
    Validate that required fields are present and non-empty
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    Returns:
        Tuple (is_valid, missing_fields)
    """
    missing = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing.append(field)
    
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    
    return True, "All required fields present"

def validate_role(role):
    """
    Validate user role
    Returns: Tuple (is_valid, error_message)
    """
    valid_roles = ['student', 'instructor', 'admin']
    
    if role not in valid_roles:
        return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
    
    return True, "Role is valid"

def validate_price(price):
    """
    Validate course price
    Returns: Tuple (is_valid, error_message)
    """
    try:
        price_float = float(price)
        if price_float < 0:
            return False, "Price cannot be negative"
        return True, "Price is valid"
    except (ValueError, TypeError):
        return False, "Price must be a valid number"

def validate_rating(rating):
    """
    Validate course rating (1-5)
    Returns: Tuple (is_valid, error_message)
    """
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return False, "Rating must be between 1 and 5"
        return True, "Rating is valid"
    except (ValueError, TypeError):
        return False, "Rating must be a valid number"

def validate_percentage(value):
    """
    Validate percentage value (0-100)
    Returns: Tuple (is_valid, error_message)
    """
    try:
        percent = float(value)
        if percent < 0 or percent > 100:
            return False, "Percentage must be between 0 and 100"
        return True, "Percentage is valid"
    except (ValueError, TypeError):
        return False, "Percentage must be a valid number"

def validate_course_data(data):
    """
    Validate course creation/update data
    Returns: Tuple (is_valid, error_message)
    """
    # Required fields
    required_fields = ['title', 'description', 'price']
    is_valid, message = validate_required_fields(data, required_fields)
    
    if not is_valid:
        return False, message
    
    # Validate price
    is_valid, message = validate_price(data['price'])
    if not is_valid:
        return False, message
    
    # Validate title length
    if len(data['title']) < 3:
        return False, "Course title must be at least 3 characters"
    
    if len(data['title']) > 200:
        return False, "Course title must be less than 200 characters"
    
    # Validate description length
    if len(data['description']) < 10:
        return False, "Course description must be at least 10 characters"
    
    return True, "Course data is valid"

def validate_enrollment_data(data):
    """
    Validate enrollment data
    Returns: Tuple (is_valid, error_message)
    """
    required_fields = ['student_id', 'course_id']
    return validate_required_fields(data, required_fields)

def sanitize_string(text, max_length=None):
    """
    Sanitize string input (remove dangerous characters)
    Args:
        text: String to sanitize
        max_length: Maximum allowed length
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Remove any potential XSS attempts
    text = str(text).strip()
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension
    Args:
        filename: Name of file to check
        allowed_extensions: Set of allowed extensions (e.g., {'pdf', 'mp4'})
    Returns:
        Boolean
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions
