"""
Check student enrollments
"""
from db_connection import get_database

# Connect to MongoDB
db = get_database()

# Find student
student = db.users.find_one({'email': 'dharunkumarm2005@gmail.com'})
if student:
    print(f"Student ID: {student['_id']}")
    print(f"Student name: {student['name']}")
    
    # Get enrollments
    enrollments = list(db.enrollments.find({'student_id': str(student['_id'])}))
    print(f"\nFound {len(enrollments)} enrollments:")
    
    for e in enrollments:
        course = db.courses.find_one({'_id': e['course_id']})
        if course:
            print(f"  - {course['title']} (ID: {e['course_id']})")
            print(f"    Status: {e['status']}, Progress: {e.get('progress', 0)}%")
        else:
            print(f"  - Course {e['course_id']} (course not found in DB)")
else:
    print("Student not found!")

