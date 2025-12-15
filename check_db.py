from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['online_course_platform']

instructors = list(db.users.find({"role": "instructor"}))
print(f"Total Instructors: {len(instructors)}")

if instructors:
    for instructor in instructors:
        print(f"\nInstructor: {instructor.get('name')}")
        print(f"Email: {instructor.get('email')}")
        instructor_id = str(instructor['_id'])
        courses = list(db.courses.find({"instructor_id": instructor_id}))
        print(f"Courses: {len(courses)}")
        for course in courses:
            print(f"  - {course.get('title')}")
else:
    print("No instructors found!")
