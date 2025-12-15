from dotenv import load_dotenv
import os
from pymongo import MongoClient
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
print('DB connected. Collections:', db.list_collection_names())
count = db.courses.count_documents({})
print('Total courses:', count)
for c in db.courses.find({}).limit(50):
    print('---')
    print('id:', str(c.get('_id')))
    print('title:', c.get('title'))
    print('is_published:', c.get('is_published'))
    print('status:', c.get('status'))
    print('instructor_id:', c.get('instructor_id'))
    print('price:', c.get('price'))
    print('materials_count:', len(c.get('materials',[])))
    print('created_at:', c.get('created_at'))
