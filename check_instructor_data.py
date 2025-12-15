"""
Quick script to check instructor data in MongoDB
"""
from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['online_course_platform']

print("=" * 60)
print("CHECKING INSTRUCTOR DATA")
print("=" * 60)

# Check for instructors
instructors = list(db.users.find({"role": "instructor"}))
print(f"\n📊 Total Instructors: {len(instructors)}")

if instructors:
    for idx, instructor in enumerate(instructors, 1):
        print(f"\n{idx}. Instructor:")
        print(f"   ID: {instructor['_id']}")
        print(f"   Name: {instructor.get('name', 'N/A')}")
        print(f"   Email: {instructor.get('email', 'N/A')}")
        print(f"   Active: {instructor.get('is_active', True)}")
        
        # Check courses for this instructor
        instructor_id = str(instructor['_id'])
        courses = list(db.courses.find({"instructor_id": instructor_id}))
        print(f"   📚 Courses: {len(courses)}")
        
        if courses:
            for course in courses:
                enrollments = db.enrollments.count_documents({
                    "course_id": str(course['_id']),
                    "status": "active"
                })
                print(f"      - {course.get('title', 'Untitled')}")
                print(f"        ID: {course['_id']}")
                print(f"        Published: {course.get('is_published', False)}")
                print(f"        Students: {enrollments}")
                print(f"        Price: ${course.get('price', 0)}")
        else:
            print(f"      ⚠️ No courses found")
else:
    print("\n❌ No instructors found in database!")
    print("\n💡 Creating a test instructor...")
    
    from werkzeug.security import generate_password_hash
    from datetime import datetime
    
    test_instructor = {
        "name": "Test Instructor",
        "email": "instructor@gmail.com",
        "password": generate_password_hash("password"),
        "role": "instructor",
        "profile_image": "",
        "bio": "Test instructor account",
        "enrolled_courses": [],
        "created_courses": [],
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = db.users.insert_one(test_instructor)
    print(f"   ✅ Created instructor with ID: {result.inserted_id}")
    print(f"   📧 Email: instructor@gmail.com")
    print(f"   🔑 Password: password")

print("\n" + "=" * 60)
print("To create a test course, run: python create_test_course.py")
print("=" * 60)
