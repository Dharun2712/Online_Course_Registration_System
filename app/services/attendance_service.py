"""
Attendance Service
Handles attendance tracking for daily logins and live class participation
"""
from datetime import datetime, timedelta
from bson import ObjectId

class AttendanceService:
    def __init__(self, db):
        self.db = db
        self.attendance_collection = db['attendance']
        self.users_collection = db['users']
        
    def mark_daily_login(self, user_id):
        """Mark daily login attendance automatically"""
        try:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Check if already marked today
            existing = self.attendance_collection.find_one({
                'user_id': ObjectId(user_id),
                'date': today,
                'type': 'daily_login'
            })
            
            if existing:
                return True, 'Attendance already marked for today'
            
            # Mark attendance
            attendance_data = {
                'user_id': ObjectId(user_id),
                'date': today,
                'type': 'daily_login',
                'marked_at': datetime.now(),
                'status': 'present'
            }
            
            self.attendance_collection.insert_one(attendance_data)
            
            # Update user's last login
            self.users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'last_login': datetime.now()}}
            )
            
            return True, 'Daily login attendance marked successfully'
            
        except Exception as e:
            return False, f'Error marking attendance: {str(e)}'
    
    def mark_live_class_attendance(self, user_id, live_class_id, course_id):
        """Mark attendance for live class participation"""
        try:
            # Check if already marked
            existing = self.attendance_collection.find_one({
                'user_id': ObjectId(user_id),
                'live_class_id': ObjectId(live_class_id),
                'type': 'live_class'
            })
            
            if existing:
                return True, 'Live class attendance already marked'
            
            attendance_data = {
                'user_id': ObjectId(user_id),
                'live_class_id': ObjectId(live_class_id),
                'course_id': ObjectId(course_id),
                'type': 'live_class',
                'marked_at': datetime.now(),
                'status': 'present'
            }
            
            self.attendance_collection.insert_one(attendance_data)
            return True, 'Live class attendance marked successfully'
            
        except Exception as e:
            return False, f'Error marking live class attendance: {str(e)}'
    
    def get_student_attendance(self, user_id, course_id=None):
        """Get attendance records for a student"""
        try:
            query = {'user_id': ObjectId(user_id)}
            if course_id:
                query['course_id'] = ObjectId(course_id)
            
            records = list(self.attendance_collection.find(query).sort('date', -1))
            
            # Format records
            for record in records:
                record['_id'] = str(record['_id'])
                record['user_id'] = str(record['user_id'])
                if 'course_id' in record:
                    record['course_id'] = str(record['course_id'])
                if 'live_class_id' in record:
                    record['live_class_id'] = str(record['live_class_id'])
                record['date'] = record.get('date', record.get('marked_at')).strftime('%Y-%m-%d')
            
            return True, records
            
        except Exception as e:
            return False, []
    
    def get_attendance_statistics(self, user_id, course_id=None):
        """Get attendance statistics for a student"""
        try:
            query = {'user_id': ObjectId(user_id)}
            if course_id:
                query['course_id'] = ObjectId(course_id)
            
            total_days = self.attendance_collection.count_documents(
                {**query, 'type': 'daily_login'}
            )
            
            live_classes = self.attendance_collection.count_documents(
                {**query, 'type': 'live_class'}
            )
            
            # Calculate percentage (assuming 30 days in a month as baseline)
            percentage = (total_days / 30) * 100 if total_days else 0
            
            return True, {
                'total_login_days': total_days,
                'live_classes_attended': live_classes,
                'attendance_percentage': min(100, round(percentage, 2))
            }
            
        except Exception as e:
            return False, {}
    
    def get_course_attendance_report(self, course_id):
        """Get attendance report for all students in a course"""
        try:
            pipeline = [
                {
                    '$match': {
                        'course_id': ObjectId(course_id),
                        'type': 'live_class'
                    }
                },
                {
                    '$group': {
                        '_id': '$user_id',
                        'total_attended': {'$sum': 1}
                    }
                },
                {
                    '$lookup': {
                        'from': 'users',
                        'localField': '_id',
                        'foreignField': '_id',
                        'as': 'user'
                    }
                },
                {'$unwind': '$user'}
            ]
            
            results = list(self.attendance_collection.aggregate(pipeline))
            
            report = []
            for r in results:
                report.append({
                    'student_id': str(r['_id']),
                    'student_name': r['user']['name'],
                    'student_email': r['user']['email'],
                    'classes_attended': r['total_attended']
                })
            
            return True, report
            
        except Exception as e:
            return False, []
