"""
Live Class Model - Zoom/Google Meet Integration
Stores live class schedules and meeting links
Supports both Zoom and Google Meet platforms
"""
from datetime import datetime
from bson import ObjectId

class LiveClass:
    def __init__(self, db):
        self.collection = db['live_classes']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for faster queries"""
        self.collection.create_index([('course_id', 1)])
        self.collection.create_index([('instructor_id', 1)])
        self.collection.create_index([('scheduled_at', 1)])
        self.collection.create_index([('status', 1)])
    
    def create_live_class(self, class_data):
        """
        Create a new live class
        class_data = {
            'course_id': ObjectId,
            'instructor_id': ObjectId,
            'title': str,
            'description': str,
            'platform': 'zoom' | 'google_meet',
            'meeting_link': str,
            'meeting_id': str,
            'meeting_password': str (optional),
            'scheduled_at': datetime,
            'duration_minutes': int,
            'status': 'scheduled|ongoing|completed|cancelled'
        }
        """
        live_class = {
            'course_id': class_data['course_id'],
            'instructor_id': class_data['instructor_id'],
            'title': class_data['title'],
            'description': class_data.get('description', ''),
            'platform': class_data['platform'],  # 'zoom' or 'google_meet'
            'meeting_link': class_data['meeting_link'],
            'meeting_id': class_data.get('meeting_id', ''),
            'meeting_password': class_data.get('meeting_password', ''),
            'scheduled_at': class_data['scheduled_at'],
            'duration_minutes': class_data.get('duration_minutes', 60),
            'status': class_data.get('status', 'scheduled'),
            'attendance_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(live_class)
        live_class['_id'] = result.inserted_id
        return self._serialize(live_class)
    
    def get_live_class(self, class_id):
        """Get live class by ID"""
        live_class = self.collection.find_one({'_id': ObjectId(class_id)})
        return self._serialize(live_class) if live_class else None
    
    def get_course_classes(self, course_id):
        """Get all live classes for a course"""
        classes = list(self.collection.find({
            'course_id': ObjectId(course_id)
        }).sort('scheduled_at', -1))
        return [self._serialize(c) for c in classes]
    
    def get_instructor_classes(self, instructor_id):
        """Get all live classes by instructor"""
        classes = list(self.collection.find({
            'instructor_id': ObjectId(instructor_id)
        }).sort('scheduled_at', -1))
        return [self._serialize(c) for c in classes]
    
    def get_upcoming_classes(self, course_id=None):
        """Get upcoming live classes"""
        query = {
            'scheduled_at': {'$gte': datetime.utcnow()},
            'status': 'scheduled'
        }
        
        if course_id:
            query['course_id'] = ObjectId(course_id)
        
        classes = list(self.collection.find(query).sort('scheduled_at', 1))
        return [self._serialize(c) for c in classes]
    
    def update_class(self, class_id, updates):
        """Update live class details"""
        updates['updated_at'] = datetime.utcnow()
        self.collection.update_one(
            {'_id': ObjectId(class_id)},
            {'$set': updates}
        )
        return self.get_live_class(class_id)
    
    def update_status(self, class_id, status):
        """Update class status"""
        return self.update_class(class_id, {'status': status})
    
    def increment_attendance(self, class_id):
        """Increment attendance count when student joins"""
        self.collection.update_one(
            {'_id': ObjectId(class_id)},
            {'$inc': {'attendance_count': 1}}
        )
        return self.get_live_class(class_id)
    
    def delete_class(self, class_id):
        """Delete live class"""
        result = self.collection.delete_one({'_id': ObjectId(class_id)})
        return result.deleted_count > 0
    
    def _serialize(self, live_class):
        """Convert ObjectId to string"""
        if live_class:
            live_class['_id'] = str(live_class['_id'])
            live_class['course_id'] = str(live_class['course_id'])
            live_class['instructor_id'] = str(live_class['instructor_id'])
        return live_class
