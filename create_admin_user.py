from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['online_course_platform']

admin_user = {
    'name': 'Admin User',
    'email': 'admin@learnhub.com',
    'password': generate_password_hash('admin123'),
    'role': 'admin',
    'is_active': True,
    'created_at': datetime.utcnow(),
    'updated_at': datetime.utcnow()
}

existing_admin = db.users.find_one({'email': admin_user['email']})

if existing_admin:
    print('Admin user already exists!')
else:
    result = db.users.insert_one(admin_user)
    print('Admin created! Email: admin@learnhub.com, Password: admin123')

client.close()
