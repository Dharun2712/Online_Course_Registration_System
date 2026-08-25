from db_connection import get_database
from werkzeug.security import generate_password_hash
from datetime import datetime

db = get_database(allow_mutation=True)

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

