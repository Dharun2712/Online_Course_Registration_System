"""
Create an instructor user for testing
"""
import sys
from db_connection import get_database
from werkzeug.security import generate_password_hash

# Connect to MongoDB
try:
    db = get_database(allow_mutation=True)
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    sys.exit(1)

# Create instructor user
instructor_data = {
    'name': 'John Instructor',
    'email': 'instructor@gmail.com',
    'password': generate_password_hash('123456'),
    'role': 'instructor',
    'is_verified': True,
    'enrolled_courses': [],
    'profile': {
        'bio': 'Experienced instructor',
        'expertise': ['Programming', 'Web Development']
    }
}

# Check if instructor already exists
existing = db.users.find_one({'email': 'instructor@gmail.com'})

if existing:
    print("📝 Instructor already exists. Updating role and password...")
    db.users.update_one(
        {'email': 'instructor@gmail.com'},
        {'$set': {
            'role': 'instructor',
            'password': generate_password_hash('123456'),
            'is_verified': True
        }}
    )
    print("✅ Updated existing user to instructor role with new password")
else:
    db.users.insert_one(instructor_data)
    print("✅ Created new instructor user")

print("\n📋 Instructor Login Credentials:")
print("Email: instructor@gmail.com")
print("Password: 123456")
print("\n🎓 You can now login as an instructor!")
