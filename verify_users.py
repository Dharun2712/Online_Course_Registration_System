"""
Verify default users in database
"""

from db_connection import get_database
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
DATABASE_NAME = os.getenv('DATABASE_NAME', 'online_course_platform')
db = get_database()

def verify_users():
    """Verify default admin and instructor accounts"""
    
    print(f"📡 Connected to database: {DATABASE_NAME}")
    print("=" * 60)
    
    # Check Admin
    admin = db.users.find_one({"email": "admin@gmail.com"})
    if admin:
        print("\n✓ Admin account found:")
        print(f"  Name: {admin.get('name')}")
        print(f"  Email: {admin.get('email')}")
        print(f"  Role: {admin.get('role')}")
        print(f"  Active: {admin.get('is_active')}")
        print(f"  Password Hash: {admin.get('password')[:30]}...")
        
        # Test password
        is_correct = check_password_hash(admin.get('password'), 'admin@123')
        print(f"  Password 'admin@123' valid: {is_correct}")
    else:
        print("\n✗ Admin account NOT found!")
    
    # Check Instructor
    instructor = db.users.find_one({"email": "instructor@gmail.com"})
    if instructor:
        print("\n✓ Instructor account found:")
        print(f"  Name: {instructor.get('name')}")
        print(f"  Email: {instructor.get('email')}")
        print(f"  Role: {instructor.get('role')}")
        print(f"  Active: {instructor.get('is_active')}")
        print(f"  Password Hash: {instructor.get('password')[:30]}...")
        
        # Test password
        is_correct = check_password_hash(instructor.get('password'), 'instructor@123')
        print(f"  Password 'instructor@123' valid: {is_correct}")
    else:
        print("\n✗ Instructor account NOT found!")
    
    # Count all users
    total_users = db.users.count_documents({})
    print(f"\n📊 Total users in database: {total_users}")
    
    # List all users
    print("\n📋 All users:")
    for user in db.users.find():
        print(f"  - {user.get('name')} ({user.get('email')}) - Role: {user.get('role')}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        verify_users()
    except Exception as e:
        print(f"Error: {str(e)}")
