from dotenv import load_dotenv
import os
from db_connection import get_database
load_dotenv()
try:
    db = get_database()
    db.client.server_info()
except Exception as e:
    print('Mongo connect error:', type(e).__name__)
    exit(1)
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
