"""
Course Model - Handles course creation and management
"""
from datetime import datetime
from bson import ObjectId

class Course:
    def __init__(self, db):
        self.collection = db['courses']
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better performance"""
        self.collection.create_index("instructor_id")
        self.collection.create_index("status")
        self.collection.create_index([("title", "text"), ("description", "text")])
        self.collection.create_index("tags")
    
    def create(self, title, description, instructor_id, price=0, tags=[], **kwargs):
        """
        Create a new course
        Args:
            title: Course title
            description: Course description
            instructor_id: ID of instructor creating the course
            price: Course price (0 for free)
            tags: List of tags/categories
        Returns:
            ObjectId of created course
        """
        course_data = {
            "title": title,
            "description": description,
            "instructor_id": str(instructor_id),
            "price": float(price),
            "tags": tags,
            "thumbnail": kwargs.get('thumbnail', ''),
            "duration": kwargs.get('duration', ''),  # e.g., "8 weeks"
            "level": kwargs.get('level', 'Beginner'),  # Beginner/Intermediate/Advanced
            "students": [],  # List of enrolled student IDs
            "materials": [],  # Course materials/lessons
            "rating": 0.0,
            "total_ratings": 0,
            "total_enrollments": 0,
            "status": "pending",  # pending/approved/rejected
            "is_published": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(course_data)
        return result.inserted_id
    
    def find_by_id(self, course_id):
        """Find course by ID"""
        try:
            course = self.collection.find_one({"_id": ObjectId(course_id)})
            if course:
                course['_id'] = str(course['_id'])
            return course
        except:
            return None
    
    def get_all_courses(self, filters=None, skip=0, limit=50):
        """
        Get courses with optional filters
        Args:
            filters: Dictionary of filters (status, tags, instructor_id, etc.)
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
        """
        query = filters if filters else {}
        courses = list(self.collection.find(query).skip(skip).limit(limit).sort("created_at", -1))
        for course in courses:
            course['_id'] = str(course['_id'])
        return courses
    
    def get_published_courses(self, skip=0, limit=50):
        """Get all approved and published courses"""
        return self.get_all_courses(
            {"status": "approved", "is_published": True},
            skip, limit
        )
    
    def search_courses(self, search_text, skip=0, limit=50):
        """Search courses by title and description"""
        courses = list(self.collection.find(
            {
                "$text": {"$search": search_text},
                "status": "approved",
                "is_published": True
            }
        ).skip(skip).limit(limit))
        
        for course in courses:
            course['_id'] = str(course['_id'])
        return courses
    
    def get_courses_by_instructor(self, instructor_id):
        """Get all courses by a specific instructor"""
        return self.get_all_courses({"instructor_id": str(instructor_id)})
    
    def get_courses_by_tags(self, tags, skip=0, limit=50):
        """Get courses by tags"""
        return self.get_all_courses(
            {"tags": {"$in": tags}, "status": "approved", "is_published": True},
            skip, limit
        )
    
    def update(self, course_id, updates):
        """Update course information"""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {"_id": ObjectId(course_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except:
            return False
    
    def approve_course(self, course_id):
        """Approve course (admin action)"""
        return self.update(course_id, {"status": "approved"})
    
    def reject_course(self, course_id, reason=""):
        """Reject course (admin action)"""
        return self.update(course_id, {"status": "rejected", "rejection_reason": reason})
    
    def publish_course(self, course_id):
        """Publish course (instructor action)"""
        return self.update(course_id, {"is_published": True})
    
    def unpublish_course(self, course_id):
        """Unpublish course (instructor action)"""
        return self.update(course_id, {"is_published": False})
    
    def enroll_student(self, course_id, student_id):
        """Add student to course"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(course_id)},
                {
                    "$addToSet": {"students": str(student_id)},
                    "$inc": {"total_enrollments": 1},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except:
            return False
    
    def add_material(self, course_id, material):
        """
        Add learning material to course
        Args:
            course_id: Course ID
            material: Dictionary with material info (title, type, url, order)
        """
        try:
            material['id'] = str(ObjectId())
            material['created_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(course_id)},
                {
                    "$push": {"materials": material},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return result.modified_count > 0
        except:
            return False
    
    def update_rating(self, course_id, new_rating):
        """Update course rating"""
        try:
            course = self.find_by_id(course_id)
            if not course:
                return False
            
            current_rating = course.get('rating', 0)
            total_ratings = course.get('total_ratings', 0)
            
            # Calculate new average rating
            new_average = ((current_rating * total_ratings) + new_rating) / (total_ratings + 1)
            
            return self.update(course_id, {
                "rating": round(new_average, 2),
                "total_ratings": total_ratings + 1
            })
        except:
            return False
    
    def delete(self, course_id):
        """Delete course"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(course_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_statistics(self, instructor_id=None):
        """Get course statistics"""
        query = {"instructor_id": str(instructor_id)} if instructor_id else {}
        
        total_courses = self.collection.count_documents(query)
        published_courses = self.collection.count_documents({**query, "is_published": True})
        
        # Aggregate total enrollments
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "total_enrollments": {"$sum": "$total_enrollments"},
                "avg_rating": {"$avg": "$rating"}
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        stats = result[0] if result else {"total_enrollments": 0, "avg_rating": 0}
        
        return {
            "total_courses": total_courses,
            "published_courses": published_courses,
            "total_enrollments": stats.get("total_enrollments", 0),
            "average_rating": round(stats.get("avg_rating", 0), 2)
        }
