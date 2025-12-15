"""
Fix enrollment data types - convert ObjectId to strings for student_id and course_id
"""
from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['online_course_platform']

# Get all enrollments
enrollments = db.enrollments.find()

updated = 0
for enrollment in enrollments:
    update_fields = {}
    
    # Check if student_id needs conversion
    if isinstance(enrollment.get('student_id'), ObjectId):
        update_fields['student_id'] = str(enrollment['student_id'])
    
    # Check if course_id needs conversion
    if isinstance(enrollment.get('course_id'), ObjectId):
        update_fields['course_id'] = str(enrollment['course_id'])
    
    # Check if payment_id needs conversion
    if enrollment.get('payment_id') and isinstance(enrollment.get('payment_id'), ObjectId):
        update_fields['payment_id'] = str(enrollment['payment_id'])
    
    # Update if needed
    if update_fields:
        db.enrollments.update_one(
            {'_id': enrollment['_id']},
            {'$set': update_fields}
        )
        updated += 1
        print(f"Updated enrollment {enrollment['_id']}: {update_fields}")

print(f"\nTotal enrollments updated: {updated}")

# Verify the fix
print("\n=== Verification ===")
enrollments_after = list(db.enrollments.find({}, {'_id': 1, 'student_id': 1, 'course_id': 1, 'status': 1}))
for e in enrollments_after:
    print(f"Enrollment {e['_id']}: student_id type={type(e['student_id'])}, course_id type={type(e['course_id'])}")

client.close()
print("\nDone!")
