"""
Script to create default admin and instructor accounts
Run this once to set up default users
"""

from db_connection import get_database
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
db = get_database(allow_mutation=True)
DATABASE_NAME = os.getenv('DATABASE_NAME', 'online_course_platform')

print(f"📡 Connecting to MongoDB database: {DATABASE_NAME}")
print("🔗 URI: configured by environment")
print()

def create_default_users():
    """Create default admin and instructor accounts"""
    
    # Default Admin
    admin_email = "admin@gmail.com"
    admin_password = "admin@123"
    
    # Default Instructor
    instructor_email = "instructor@gmail.com"
    instructor_password = "instructor@123"
    
    # Check if admin already exists
    existing_admin = db.users.find_one({"email": admin_email})
    if existing_admin:
        print(f"✓ Admin account already exists: {admin_email}")
    else:
        # Create admin
        admin_user = {
            "name": "System Administrator",
            "email": admin_email,
            "password": generate_password_hash(admin_password),
            "role": "admin",
            "created_at": datetime.utcnow(),
            "is_active": True,
            "profile": {
                "bio": "System Administrator",
                "avatar": "",
                "phone": ""
            }
        }
        result = db.users.insert_one(admin_user)
        print(f"✓ Admin account created successfully!")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
        print(f"  ID: {result.inserted_id}")
    
    # Check if instructor already exists
    existing_instructor = db.users.find_one({"email": instructor_email})
    if existing_instructor:
        print(f"\n✓ Instructor account already exists: {instructor_email}")
    else:
        # Create instructor
        instructor_user = {
            "name": "Default Instructor",
            "email": instructor_email,
            "password": generate_password_hash(instructor_password),
            "role": "instructor",
            "created_at": datetime.utcnow(),
            "is_active": True,
            "profile": {
                "bio": "Default instructor account for testing and demonstrations",
                "avatar": "",
                "phone": "",
                "expertise": ["Teaching", "Education", "Course Development"],
                "qualifications": "Master's in Education"
            }
        }
        result = db.users.insert_one(instructor_user)
        print(f"✓ Instructor account created successfully!")
        print(f"  Email: {instructor_email}")
        print(f"  Password: {instructor_password}")
        print(f"  ID: {result.inserted_id}")
    
    print("\n" + "="*60)
    print("Default Users Setup Complete!")
    print("="*60)
    print("\nLogin Credentials:")
    print(f"Admin     - Email: {admin_email} | Password: {admin_password}")
    print(f"Instructor - Email: {instructor_email} | Password: {instructor_password}")
    print("\nYou can now login with these credentials from the homepage.")
    print("="*60)

if __name__ == "__main__":
    try:
        create_default_users()
    except Exception as e:
        print(f"Error creating default users: {str(e)}")
