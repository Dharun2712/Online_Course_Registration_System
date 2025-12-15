from dotenv import load_dotenv
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
load_dotenv()
uri = os.getenv('MONGO_URI')
if not uri:
    print('No MONGO_URI set')
    exit(1)
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
try:
    client.server_info()
except Exception as e:
    print('Mongo connect error:', e)
    exit(1)
db = client[os.getenv('DATABASE_NAME','online_course_platform')]

# Create default users
users = db.users
instructor_email = 'instructor@gmail.com'
admin_email = 'admin@gmail.com'

instr = users.find_one({'email': instructor_email})
if not instr:
    instr_id = users.insert_one({
        'name': 'Default Instructor',
        'email': instructor_email,
        'password': generate_password_hash('instructor@123'),
        'role': 'instructor',
        'created_at': datetime.utcnow()
    }).inserted_id
    print('Inserted instructor:', instructor_email)
else:
    instr_id = instr['_id']
    print('Instructor already exists')

adm = users.find_one({'email': admin_email})
if not adm:
    admin_id = users.insert_one({
        'name': 'Admin',
        'email': admin_email,
        'password': generate_password_hash('admin@123'),
        'role': 'admin',
        'created_at': datetime.utcnow()
    }).inserted_id
    print('Inserted admin:', admin_email)
else:
    admin_id = adm['_id']
    print('Admin already exists')

# Insert sample courses
courses = db.courses
if courses.count_documents({}) == 0:
    sample = [
        {
            'title': 'Introduction to Python',
            'description': 'Learn Python from scratch. Variables, control flow, functions, and more.',
            'instructor_id': str(instr_id),
            'price': 0,
            'tags': ['programming','python'],
            'thumbnail': '',
            'duration': '10 hours',
            'level': 'Beginner',
            'materials': [],
            'status': 'approved',
            'is_published': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'title': 'Web Development with Flask',
            'description': 'Build web apps using Flask, Jinja, and MongoDB.',
            'instructor_id': str(instr_id),
            'price': 29.99,
            'tags': ['web','flask','python'],
            'thumbnail': '',
            'duration': '15 hours',
            'level': 'Intermediate',
            'materials': [],
            'status': 'approved',
            'is_published': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'title': 'Data Analysis with Pandas',
            'description': 'Analyze and visualize data using pandas and matplotlib.',
            'instructor_id': str(instr_id),
            'price': 19.99,
            'tags': ['data','pandas'],
            'thumbnail': '',
            'duration': '8 hours',
            'level': 'Beginner',
            'materials': [],
            'status': 'approved',
            'is_published': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]
    result = courses.insert_many(sample)
    print('Inserted sample courses:', result.inserted_ids)
else:
    print('Courses already present, skipping insertion')

print('Done')
