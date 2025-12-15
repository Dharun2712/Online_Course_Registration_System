"""
Progress Model - Tracks detailed student learning progress
"""
from datetime import datetime
from bson import ObjectId

class Progress:
    def __init__(self, db):
        self.collection = db['progress']
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better performance"""
        self.collection.create_index([("student_id", 1), ("course_id", 1), ("material_id", 1)])
        self.collection.create_index("student_id")
        self.collection.create_index("course_id")
    
    def update(self, student_id, course_id, material_id, progress_data):
        """
        Update or create progress record for a specific material
        Args:
            student_id: Student ID
            course_id: Course ID
            material_id: Course material ID
            progress_data: Dictionary with progress info (time_spent, completed, etc.)
        """
        try:
            record = {
                "student_id": str(student_id),
                "course_id": str(course_id),
                "material_id": str(material_id),
                "time_spent": progress_data.get('time_spent', 0),  # in minutes
                "completed": progress_data.get('completed', False),
                "last_position": progress_data.get('last_position', 0),  # for videos
                "quiz_score": progress_data.get('quiz_score'),
                "notes": progress_data.get('notes', ''),
                "updated_at": datetime.utcnow()
            }
            
            result = self.collection.update_one(
                {
                    "student_id": str(student_id),
                    "course_id": str(course_id),
                    "material_id": str(material_id)
                },
                {"$set": record},
                upsert=True
            )
            return True
        except:
            return False
    
    def get_progress(self, student_id, course_id, material_id=None):
        """Get progress for a student in a course or specific material"""
        query = {
            "student_id": str(student_id),
            "course_id": str(course_id)
        }
        
        if material_id:
            query["material_id"] = str(material_id)
            progress = self.collection.find_one(query)
            if progress:
                progress['_id'] = str(progress['_id'])
            return progress
        else:
            # Get all progress records for the course
            records = list(self.collection.find(query))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
    
    def get_course_completion_percentage(self, student_id, course_id):
        """Calculate completion percentage for a course"""
        total = self.collection.count_documents({
            "student_id": str(student_id),
            "course_id": str(course_id)
        })
        
        if total == 0:
            return 0
        
        completed = self.collection.count_documents({
            "student_id": str(student_id),
            "course_id": str(course_id),
            "completed": True
        })
        
        return round((completed / total) * 100, 2)
    
    def get_total_time_spent(self, student_id, course_id=None):
        """Get total time spent by student"""
        query = {"student_id": str(student_id)}
        if course_id:
            query["course_id"] = str(course_id)
        
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "total_time": {"$sum": "$time_spent"}
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result[0].get("total_time", 0) if result else 0
    
    def mark_completed(self, student_id, course_id, material_id):
        """Mark a material as completed"""
        return self.update(student_id, course_id, material_id, {"completed": True})
    
    def save_video_position(self, student_id, course_id, material_id, position):
        """Save last video playback position"""
        return self.update(student_id, course_id, material_id, {"last_position": position})
    
    def save_quiz_score(self, student_id, course_id, material_id, score):
        """Save quiz score"""
        return self.update(student_id, course_id, material_id, {
            "quiz_score": score,
            "completed": score >= 70  # 70% passing score
        })
    
    def get_learning_analytics(self, student_id):
        """Get detailed learning analytics for a student"""
        pipeline = [
            {"$match": {"student_id": str(student_id)}},
            {"$group": {
                "_id": "$course_id",
                "total_materials": {"$sum": 1},
                "completed_materials": {
                    "$sum": {"$cond": [{"$eq": ["$completed", True]}, 1, 0]}
                },
                "total_time": {"$sum": "$time_spent"},
                "avg_quiz_score": {"$avg": "$quiz_score"}
            }}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        analytics = []
        for result in results:
            completion_rate = (result['completed_materials'] / result['total_materials'] * 100) if result['total_materials'] > 0 else 0
            analytics.append({
                "course_id": result['_id'],
                "total_materials": result['total_materials'],
                "completed_materials": result['completed_materials'],
                "completion_rate": round(completion_rate, 2),
                "total_time_spent": result['total_time'],
                "average_quiz_score": round(result.get('avg_quiz_score', 0), 2) if result.get('avg_quiz_score') else None
            })
        
        return analytics
    
    def delete_course_progress(self, student_id, course_id):
        """Delete all progress records for a course"""
        try:
            result = self.collection.delete_many({
                "student_id": str(student_id),
                "course_id": str(course_id)
            })
            return result.deleted_count > 0
        except:
            return False
