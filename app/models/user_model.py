"""
User Model - Handles user authentication and management
Supports three roles: student, instructor, admin
"""
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, db):
        self.collection = db['users']
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better performance"""
        self.collection.create_index("email", unique=True)
        self.collection.create_index("role")
    
    def create(self, name, email, password, role='student', **kwargs):
        """
        Create a new user
        Args:
            name: User's full name
            email: Unique email address
            password: Plain text password (will be hashed)
            role: student/instructor/admin
        Returns:
            ObjectId of created user or None if email exists
        """
        # Check if email already exists
        if self.collection.find_one({"email": email}):
            return None
        
        hashed_password = generate_password_hash(password)
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "profile_image": kwargs.get('profile_image', ''),
            "bio": kwargs.get('bio', ''),
            "enrolled_courses": [],  # For students
            "created_courses": [],   # For instructors
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(user_data)
        return result.inserted_id
    
    def authenticate(self, email, password):
        """
        Authenticate user with email and password
        Returns:
            User document without password if successful, None otherwise
        """
        user = self.collection.find_one({"email": email})
        
        if user and check_password_hash(user["password"], password):
            # Remove password from returned user object
            user.pop('password', None)
            user['_id'] = str(user['_id'])
            return user
        
        return None
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user.pop('password', None)
                user['_id'] = str(user['_id'])
            return user
        except:
            return None
    
    def find_by_email(self, email):
        """Find user by email"""
        user = self.collection.find_one({"email": email})
        if user:
            user.pop('password', None)
            user['_id'] = str(user['_id'])
        return user
    
    def update(self, user_id, updates):
        """Update user information"""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except:
            return False
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})
            if user and check_password_hash(user['password'], old_password):
                hashed = generate_password_hash(new_password)
                self.collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"password": hashed, "updated_at": datetime.utcnow()}}
                )
                return True
            return False
        except:
            return False
    
    def get_all_users(self, role=None, skip=0, limit=50):
        """Get all users with optional role filter"""
        query = {"role": role} if role else {}
        users = list(self.collection.find(query).skip(skip).limit(limit))
        for user in users:
            user.pop('password', None)
            user['_id'] = str(user['_id'])
        return users
    
    def delete(self, user_id):
        """Soft delete user (deactivate)"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def add_enrolled_course(self, user_id, course_id):
        """Add course to student's enrolled list"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$addToSet": {"enrolled_courses": str(course_id)}}
            )
            return result.modified_count > 0
        except:
            return False
