from db_connection import get_database
from pprint import pprint

db = get_database()
exams = list(db.exams.find().sort('created_at', -1).limit(10))
print('Found', len(exams), 'exams')
for e in exams:
    print('---')
    pprint({
        '_id': str(e.get('_id')),
        'title': e.get('title'),
        'exam_date': e.get('exam_date'),
        'deadline': e.get('deadline'),
        'exam_date_type': type(e.get('exam_date')).__name__ if e.get('exam_date') is not None else None
    })
