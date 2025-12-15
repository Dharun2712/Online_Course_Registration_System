"""
Check users and their roles
"""
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['online_course_platform']

print("=== Users in Database ===\n")

users = db.users.find({}, {'name': 1, 'email': 1, 'role': 1})

for user in users:
    print(f"Name: {user.get('name', 'N/A')}")
    print(f"Email: {user.get('email', 'N/A')}")
    print(f"Role: {user.get('role', 'N/A')}")
    print(f"ID: {user['_id']}")
    print("-" * 50)

# Check courses
print("\n=== Courses in Database ===\n")
courses = db.courses.find({}, {'title': 1, 'instructor_id': 1, 'is_published': 1})
course_count = db.courses.count_documents({})
print(f"Total courses: {course_count}\n")

for course in courses:
    print(f"Title: {course.get('title', 'N/A')}")
    print(f"Instructor ID: {course.get('instructor_id', 'N/A')}")
    print(f"Published: {course.get('is_published', False)}")
    print(f"Course ID: {course['_id']}")
    print("-" * 50)
