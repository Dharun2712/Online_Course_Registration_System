from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['online_course_platform']

# Find a course and an instructor to attach the exam to
course = db.courses.find_one()
instructor = db.users.find_one({'role':'instructor'}) or db.users.find_one()

if not course or not instructor:
    print('Missing course or instructor in DB. Ensure at least one course and one instructor exist.')
else:
    now = datetime.now()
    exam_date = now - timedelta(minutes=5)  # started 5 minutes ago
    deadline = now + timedelta(days=4)      # ends in 4 days

    exam_doc = {
        'course_id': course['_id'],
        'instructor_id': instructor['_id'],
        'title': 'Automated Test Exam (Available Now)',
        'description': 'Inserted by integration test script',
        'questions': [],
        'total_marks': 10,
        'passing_marks': 5,
        'passing_score_percent': 50,
        'duration_minutes': 60,
        'status': 'active',
        'is_published': True,
        'exam_date': exam_date,
        'deadline': deadline,
        'created_at': now,
        'updated_at': now
    }

    res = db.exams.insert_one(exam_doc)
    print('Inserted exam id:', str(res.inserted_id))
    pprint({
        'exam_date': exam_date,
        'deadline': deadline,
        'now': now
    })
