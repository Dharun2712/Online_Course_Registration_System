"""
Enrollment Model - Handles student course enrollments
"""
from datetime import datetime
from bson import ObjectId

class Enrollment:
    def __init__(self, db):
        self.collection = db['enrollments']
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better performance"""
        self.collection.create_index([("student_id", 1), ("course_id", 1)], unique=True)
        self.collection.create_index("student_id")
        self.collection.create_index("course_id")
        self.collection.create_index("status")
    
    def enroll(self, student_id, course_id, payment_id=None):
        """
        Enroll student in a course
        Args:
            student_id: Student's user ID
            course_id: Course ID
            payment_id: Payment record ID (if paid course)
        Returns:
            ObjectId of enrollment or None if already enrolled
        """
        # Check if already enrolled
        existing = self.collection.find_one({
            "student_id": str(student_id),
            "course_id": str(course_id)
        })
        
        if existing:
            return None
        
        enrollment_data = {
            "student_id": str(student_id),
            "course_id": str(course_id),
            "payment_id": str(payment_id) if payment_id else None,
            "progress": 0,  # Percentage (0-100)
            "completed_materials": [],  # List of completed material IDs
            "status": "active",  # active/completed/dropped
            "certificate_issued": False,
            "enrolled_at": datetime.utcnow(),
            "completed_at": None,
            "last_accessed": datetime.utcnow()
        }
        
        result = self.collection.insert_one(enrollment_data)
        return result.inserted_id
    
    def find_by_id(self, enrollment_id):
        """Find enrollment by ID"""
        try:
            enrollment = self.collection.find_one({"_id": ObjectId(enrollment_id)})
            if enrollment:
                enrollment['_id'] = str(enrollment['_id'])
            return enrollment
        except:
            return None
    
    def get_student_enrollments(self, student_id, status=None):
        """Get all enrollments for a student"""
        query = {"student_id": str(student_id)}
        if status:
            query["status"] = status
        
        enrollments = list(self.collection.find(query).sort("enrolled_at", -1))
        for enrollment in enrollments:
            enrollment['_id'] = str(enrollment['_id'])
        return enrollments
    
    def get_course_enrollments(self, course_id):
        """Get all enrollments for a course"""
        enrollments = list(self.collection.find({"course_id": str(course_id)}).sort("enrolled_at", -1))
        for enrollment in enrollments:
            enrollment['_id'] = str(enrollment['_id'])
        return enrollments
    
    def is_enrolled(self, student_id, course_id):
        """Check if student is enrolled in a course"""
        enrollment = self.collection.find_one({
            "student_id": str(student_id),
            "course_id": str(course_id)
        })
        return enrollment is not None
    
    def update_progress(self, student_id, course_id, progress_percent):
        """
        Update student's progress in a course
        Args:
            student_id: Student ID
            course_id: Course ID
            progress_percent: Progress percentage (0-100)
        """
        try:
            updates = {
                "progress": min(100, max(0, progress_percent)),
                "last_accessed": datetime.utcnow()
            }
            
            # If 100% complete, mark as completed
            if progress_percent >= 100:
                updates["status"] = "completed"
                updates["completed_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {
                    "student_id": str(student_id),
                    "course_id": str(course_id)
                },
                {"$set": updates}
            )
            return result.modified_count > 0
        except:
            return False
    
    def mark_material_completed(self, student_id, course_id, material_id):
        """Mark a course material as completed"""
        try:
            result = self.collection.update_one(
                {
                    "student_id": str(student_id),
                    "course_id": str(course_id)
                },
                {
                    "$addToSet": {"completed_materials": str(material_id)},
                    "$set": {"last_accessed": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except:
            return False
    
    def drop_course(self, student_id, course_id):
        """Drop/unenroll from a course"""
        try:
            result = self.collection.update_one(
                {
                    "student_id": str(student_id),
                    "course_id": str(course_id)
                },
                {"$set": {"status": "dropped", "last_accessed": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def issue_certificate(self, student_id, course_id):
        """Issue certificate for completed course"""
        try:
            enrollment = self.collection.find_one({
                "student_id": str(student_id),
                "course_id": str(course_id),
                "status": "completed"
            })
            
            if not enrollment:
                return False
            
            result = self.collection.update_one(
                {"_id": enrollment["_id"]},
                {"$set": {"certificate_issued": True}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def get_statistics(self, student_id=None, course_id=None):
        """Get enrollment statistics"""
        query = {}
        if student_id:
            query["student_id"] = str(student_id)
        if course_id:
            query["course_id"] = str(course_id)
        
        total = self.collection.count_documents(query)
        active = self.collection.count_documents({**query, "status": "active"})
        completed = self.collection.count_documents({**query, "status": "completed"})
        
        # Calculate average progress
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "avg_progress": {"$avg": "$progress"}
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        avg_progress = result[0].get("avg_progress", 0) if result else 0
        
        return {
            "total_enrollments": total,
            "active_enrollments": active,
            "completed_enrollments": completed,
            "average_progress": round(avg_progress, 2)
        }
    
    def delete(self, enrollment_id):
        """Delete enrollment record"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(enrollment_id)})
            return result.deleted_count > 0
        except:
            return False
