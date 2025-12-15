"""
Live Class Service
Handles live class scheduling and Zoom/Google Meet integration
"""
from datetime import datetime
from bson import ObjectId
import secrets

class LiveClassService:
    def __init__(self, db):
        self.db = db
        self.liveclass_collection = db['live_classes']
        self.course_collection = db['courses']
        
    def schedule_live_class(self, course_id, instructor_id, class_data):
        """Schedule a new live class"""
        try:
            # Get datetime (support both starts_at and scheduled_at)
            starts_at = class_data.get('starts_at') or class_data.get('scheduled_at')
            if not starts_at:
                return False, 'Start time is required'
            
            # Parse datetime string
            if isinstance(starts_at, str):
                # Handle both formats: "2025-11-14T10:36" or ISO format
                if 'T' in starts_at and len(starts_at) == 16:  # "2025-11-14T10:36"
                    starts_at = starts_at + ':00'  # Add seconds
                starts_at_dt = datetime.fromisoformat(starts_at)
            else:
                starts_at_dt = starts_at
            
            # Get platform/meeting type
            meeting_type = class_data.get('meeting_type') or class_data.get('platform', 'zoom')
            
            # Map meeting types
            platform_map = {
                'meet': 'google_meet',
                'zoom': 'zoom',
                'teams': 'teams',
                'custom': 'custom'
            }
            platform = platform_map.get(meeting_type, meeting_type)
            
            # Get or generate meeting link
            meeting_link = class_data.get('meeting_link', '')
            if not meeting_link and platform in ['zoom', 'google_meet']:
                meeting_link = self._generate_meeting_link(platform, class_data)
            
            class_doc = {
                'course_id': str(course_id) if not isinstance(course_id, ObjectId) else course_id,
                'instructor_id': str(instructor_id) if not isinstance(instructor_id, ObjectId) else instructor_id,
                'title': class_data.get('title'),
                'description': class_data.get('description', ''),
                'meeting_type': meeting_type,
                'platform': platform,
                'meeting_link': meeting_link,
                'meeting_id': class_data.get('meeting_id', self._generate_meeting_id()),
                'password': class_data.get('password', self._generate_password()),
                'starts_at': starts_at_dt,
                'scheduled_at': starts_at_dt,  # Keep both for compatibility
                'duration_minutes': class_data.get('duration_minutes', 60),
                'status': 'scheduled',
                'created_at': datetime.now(),
                'attendees': []
            }
            
            result = self.liveclass_collection.insert_one(class_doc)
            
            return True, str(result.inserted_id)
            
        except Exception as e:
            return False, f'Error scheduling live class: {str(e)}'
    
    def _generate_meeting_link(self, platform, class_data):
        """Generate meeting link (placeholder for actual API integration)"""
        meeting_id = class_data.get('meeting_id', self._generate_meeting_id())
        
        if platform == 'zoom':
            return f"https://zoom.us/j/{meeting_id}"
        elif platform == 'google_meet':
            code = secrets.token_urlsafe(10)
            return f"https://meet.google.com/{code}"
        
        return ""
    
    def _generate_meeting_id(self):
        """Generate random meeting ID"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(11)])
    
    def _generate_password(self):
        """Generate random meeting password"""
        return secrets.token_urlsafe(8)
    
    def get_live_class(self, class_id):
        """Get live class details"""
        try:
            live_class = self.liveclass_collection.find_one({'_id': ObjectId(class_id)})
            
            if not live_class:
                return False, None
            
            live_class['_id'] = str(live_class['_id'])
            live_class['course_id'] = str(live_class['course_id'])
            live_class['instructor_id'] = str(live_class['instructor_id'])
            live_class['scheduled_at'] = live_class['scheduled_at'].isoformat()
            
            return True, live_class
            
        except Exception as e:
            return False, None
    
    def get_course_live_classes(self, course_id):
        """Get all live classes for a course"""
        try:
            # Handle both ObjectId and string formats
            # Live classes store course_id as string
            query_id = str(course_id) if course_id else None
            if not query_id:
                return False, []
            
            # Try to find by course_id (try both as string and ObjectId)
            classes = list(self.liveclass_collection.find({
                'course_id': query_id
            }).sort('starts_at', -1))
            
            for cls in classes:
                cls['_id'] = str(cls['_id'])
                # Ensure IDs are strings
                if isinstance(cls.get('course_id'), ObjectId):
                    cls['course_id'] = str(cls['course_id'])
                if isinstance(cls.get('instructor_id'), ObjectId):
                    cls['instructor_id'] = str(cls['instructor_id'])
                # Handle datetime for scheduled_at and starts_at
                if 'scheduled_at' in cls and cls['scheduled_at']:
                    cls['scheduled_at'] = cls['scheduled_at'].isoformat() if hasattr(cls['scheduled_at'], 'isoformat') else str(cls['scheduled_at'])
                if 'starts_at' in cls and cls['starts_at']:
                    cls['starts_at'] = cls['starts_at'].isoformat() if hasattr(cls['starts_at'], 'isoformat') else str(cls['starts_at'])
                # Ensure starts_at exists (fallback to scheduled_at)
                if 'starts_at' not in cls and 'scheduled_at' in cls:
                    cls['starts_at'] = cls['scheduled_at']
            
            return True, classes
            
        except Exception as e:
            print(f"Error in get_course_live_classes: {e}")
            return False, []
    
    def get_upcoming_classes(self, user_id, role='student'):
        """Get upcoming live classes for a user"""
        try:
            now = datetime.now()
            
            if role == 'student':
                # Get enrolled courses
                enrollments = list(self.db['enrollments'].find({
                    'student_id': ObjectId(user_id)
                }))
                course_ids = [e['course_id'] for e in enrollments]
                
                classes = list(self.liveclass_collection.find({
                    'course_id': {'$in': course_ids},
                    'scheduled_at': {'$gte': now}
                }).sort('scheduled_at', 1).limit(10))
                
            elif role == 'instructor':
                classes = list(self.liveclass_collection.find({
                    'instructor_id': ObjectId(user_id),
                    'scheduled_at': {'$gte': now}
                }).sort('scheduled_at', 1).limit(10))
            else:
                classes = list(self.liveclass_collection.find({
                    'scheduled_at': {'$gte': now}
                }).sort('scheduled_at', 1).limit(20))
            
            # Get course details
            for cls in classes:
                course = self.course_collection.find_one({'_id': cls['course_id']})
                cls['_id'] = str(cls['_id'])
                cls['course_id'] = str(cls['course_id'])
                cls['instructor_id'] = str(cls['instructor_id'])
                cls['course_title'] = course['title'] if course else 'Unknown'
                cls['scheduled_at'] = cls['scheduled_at'].isoformat()
            
            return True, classes
            
        except Exception as e:
            return False, []
    
    def update_live_class(self, class_id, update_data):
        """Update live class details"""
        try:
            update_fields = {}
            
            if 'title' in update_data:
                update_fields['title'] = update_data['title']
            if 'description' in update_data:
                update_fields['description'] = update_data['description']
            if 'scheduled_at' in update_data:
                update_fields['scheduled_at'] = datetime.fromisoformat(update_data['scheduled_at'])
            if 'duration_minutes' in update_data:
                update_fields['duration_minutes'] = update_data['duration_minutes']
            if 'status' in update_data:
                update_fields['status'] = update_data['status']
            
            if update_fields:
                update_fields['updated_at'] = datetime.now()
                
                result = self.liveclass_collection.update_one(
                    {'_id': ObjectId(class_id)},
                    {'$set': update_fields}
                )
                
                if result.modified_count > 0:
                    return True, 'Live class updated successfully'
                else:
                    return False, 'No changes made'
            else:
                return False, 'No update data provided'
            
        except Exception as e:
            return False, f'Error updating live class: {str(e)}'
    
    def delete_live_class(self, class_id):
        """Delete a live class"""
        try:
            result = self.liveclass_collection.delete_one({'_id': ObjectId(class_id)})
            
            if result.deleted_count > 0:
                return True, 'Live class deleted successfully'
            else:
                return False, 'Live class not found'
            
        except Exception as e:
            return False, f'Error deleting live class: {str(e)}'
    
    def mark_attendance(self, class_id, student_id):
        """Mark student attendance for live class"""
        try:
            result = self.liveclass_collection.update_one(
                {'_id': ObjectId(class_id)},
                {
                    '$addToSet': {'attendees': ObjectId(student_id)},
                    '$set': {'last_attendance_marked': datetime.now()}
                }
            )
            
            if result.modified_count > 0:
                return True, 'Attendance marked successfully'
            else:
                return False, 'Already marked or class not found'
            
        except Exception as e:
            return False, f'Error marking attendance: {str(e)}'
    
    def get_class_attendees(self, class_id):
        """Get list of attendees for a live class"""
        try:
            live_class = self.liveclass_collection.find_one({'_id': ObjectId(class_id)})
            
            if not live_class:
                return False, []
            
            attendee_ids = live_class.get('attendees', [])
            attendees = list(self.db['users'].find({
                '_id': {'$in': attendee_ids}
            }))
            
            result = []
            for user in attendees:
                result.append({
                    'user_id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email']
                })
            
            return True, result
            
        except Exception as e:
            return False, []
