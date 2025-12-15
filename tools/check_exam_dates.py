from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

client = MongoClient('mongodb://localhost:27017')
db = client['online_course_platform']

# Get the most recent exam
exam = db.exams.find_one(sort=[('created_at', -1)])

if exam:
    print("=== MOST RECENT EXAM ===")
    print(f"Title: {exam.get('title')}")
    print(f"Exam Date: {exam.get('exam_date')} (Type: {type(exam.get('exam_date'))})")
    print(f"Deadline: {exam.get('deadline')} (Type: {type(exam.get('deadline'))})")
    print(f"Created At: {exam.get('created_at')}")
    print(f"\nCurrent Server Time: {datetime.now()}")
    
    # Check if dates exist and are valid
    exam_date = exam.get('exam_date')
    deadline = exam.get('deadline')
    now = datetime.now()
    
    if exam_date and deadline:
        print(f"\nComparison:")
        print(f"  Now >= Exam Date: {now >= exam_date}")
        print(f"  Now <= Deadline: {now <= deadline}")
        print(f"  Should be AVAILABLE: {now >= exam_date and now <= deadline}")
    else:
        print("\n⚠️ Exam dates are missing!")
else:
    print("No exams found")
