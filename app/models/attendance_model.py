"""
Attendance Model - Track Daily Login and Live Class Attendance
Auto-marks attendance on daily student login
Tracks live class participation
"""
from datetime import datetime, date
from bson import ObjectId

class Attendance:
    def __init__(self, db):
        self.collection = db['attendance']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for faster queries"""
        self.collection.create_index([('student_id', 1), ('date', 1)])
        self.collection.create_index([('course_id', 1)])
        self.collection.create_index([('live_class_id', 1)])
    
    def mark_daily_login(self, student_id):
        """
        Auto-mark attendance on daily login
        Only marks once per day
        """
        today = date.today()
        
        # Check if already marked today
        existing = self.collection.find_one({
            'student_id': ObjectId(student_id),
            'date': today,
            'type': 'daily_login'
        })
        
        if existing:
            return self._serialize(existing)
        
        # Mark new attendance
        attendance = {
            'student_id': ObjectId(student_id),
            'date': today,
            'type': 'daily_login',
            'present': True,
            'marked_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(attendance)
        attendance['_id'] = result.inserted_id
        return self._serialize(attendance)
    
    def mark_live_class_attendance(self, attendance_data):
        """
        Mark attendance for live class participation
        attendance_data = {
            'student_id': ObjectId,
            'course_id': ObjectId,
            'live_class_id': ObjectId,
            'class_title': str,
            'joined_at': datetime
        }
        """
        # Check if already marked
        existing = self.collection.find_one({
            'student_id': ObjectId(attendance_data['student_id']),
            'live_class_id': ObjectId(attendance_data['live_class_id'])
        })
        
        if existing:
            return self._serialize(existing)
        
        attendance = {
            'student_id': attendance_data['student_id'],
            'course_id': attendance_data['course_id'],
            'live_class_id': attendance_data['live_class_id'],
            'class_title': attendance_data.get('class_title', ''),
            'date': date.today(),
            'type': 'live_class',
            'present': True,
            'joined_at': attendance_data.get('joined_at', datetime.utcnow()),
            'marked_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(attendance)
        attendance['_id'] = result.inserted_id
        return self._serialize(attendance)
    
    def get_student_attendance(self, student_id, start_date=None, end_date=None):
        """Get student attendance records"""
        query = {'student_id': ObjectId(student_id)}
        
        if start_date and end_date:
            query['date'] = {'$gte': start_date, '$lte': end_date}
        
        records = list(self.collection.find(query).sort('date', -1))
        return [self._serialize(record) for record in records]
    
    def get_course_attendance(self, course_id, student_id=None):
        """Get attendance for a specific course"""
        query = {'course_id': ObjectId(course_id)}
        
        if student_id:
            query['student_id'] = ObjectId(student_id)
        
        records = list(self.collection.find(query).sort('date', -1))
        return [self._serialize(record) for record in records]
    
    def get_attendance_stats(self, student_id, course_id=None):
        """Get attendance statistics"""
        query = {'student_id': ObjectId(student_id)}
        
        if course_id:
            query['course_id'] = ObjectId(course_id)
        
        total_days = self.collection.count_documents({**query, 'type': 'daily_login'})
        total_classes = self.collection.count_documents({**query, 'type': 'live_class'})
        
        return {
            'total_daily_logins': total_days,
            'total_live_classes_attended': total_classes,
            'total_attendance': total_days + total_classes
        }
    
    def get_class_attendance_list(self, live_class_id):
        """Get list of students who attended a live class"""
        records = list(self.collection.find({
            'live_class_id': ObjectId(live_class_id),
            'type': 'live_class'
        }))
        return [self._serialize(record) for record in records]
    
    def _serialize(self, record):
        """Convert ObjectId to string"""
        if record:
            record['_id'] = str(record['_id'])
            record['student_id'] = str(record['student_id'])
            if 'course_id' in record:
                record['course_id'] = str(record['course_id'])
            if 'live_class_id' in record:
                record['live_class_id'] = str(record['live_class_id'])
            # Convert date to string
            if 'date' in record and isinstance(record['date'], date):
                record['date'] = record['date'].isoformat()
        return record
