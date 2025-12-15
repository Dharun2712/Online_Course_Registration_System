"""
Analytics Service
Provides comprehensive analytics and reporting for all user roles
"""
from datetime import datetime, timedelta
from bson import ObjectId

class AnalyticsService:
    def __init__(self, db):
        self.db = db
        
    def get_student_analytics(self, student_id):
        """Get comprehensive analytics for a student"""
        try:
            # Enrollments
            enrollments = self.db['enrollments'].count_documents({
                'student_id': ObjectId(student_id)
            })
            
            # Completed courses
            completed = self.db['enrollments'].count_documents({
                'student_id': ObjectId(student_id),
                'completed': True
            })
            
            # Average progress
            pipeline_progress = [
                {'$match': {'student_id': ObjectId(student_id)}},
                {'$group': {
                    '_id': None,
                    'avg_progress': {'$avg': '$progress'}
                }}
            ]
            progress_result = list(self.db['enrollments'].aggregate(pipeline_progress))
            avg_progress = progress_result[0]['avg_progress'] if progress_result else 0
            
            # Exam results
            exams_taken = self.db['exam_submissions'].count_documents({
                'student_id': ObjectId(student_id)
            })
            
            exams_passed = self.db['exam_submissions'].count_documents({
                'student_id': ObjectId(student_id),
                'passed': True
            })
            
            # Average marks
            pipeline_marks = [
                {'$match': {'student_id': ObjectId(student_id), 'graded': True}},
                {'$group': {
                    '_id': None,
                    'avg_percentage': {
                        '$avg': {
                            '$multiply': [
                                {'$divide': ['$marks_obtained', '$total_marks']},
                                100
                            ]
                        }
                    }
                }}
            ]
            marks_result = list(self.db['exam_submissions'].aggregate(pipeline_marks))
            avg_percentage = marks_result[0]['avg_percentage'] if marks_result else 0
            
            # Certificates
            certificates = self.db['certificates'].count_documents({
                'student_id': ObjectId(student_id),
                'status': 'active'
            })
            
            # Attendance
            attendance_days = self.db['attendance'].count_documents({
                'user_id': ObjectId(student_id),
                'type': 'daily_login'
            })
            
            live_classes = self.db['attendance'].count_documents({
                'user_id': ObjectId(student_id),
                'type': 'live_class'
            })
            
            # Payment history
            pipeline_payments = [
                {'$match': {'student_id': ObjectId(student_id), 'status': 'completed'}},
                {'$group': {
                    '_id': None,
                    'total_spent': {'$sum': '$amount'}
                }}
            ]
            payment_result = list(self.db['payments'].aggregate(pipeline_payments))
            total_spent = payment_result[0]['total_spent'] if payment_result else 0
            
            return True, {
                'enrollments': enrollments,
                'completed_courses': completed,
                'average_progress': round(avg_progress, 2),
                'exams_taken': exams_taken,
                'exams_passed': exams_passed,
                'pass_rate': round((exams_passed / exams_taken * 100), 2) if exams_taken > 0 else 0,
                'average_percentage': round(avg_percentage, 2),
                'certificates_earned': certificates,
                'attendance_days': attendance_days,
                'live_classes_attended': live_classes,
                'total_spent': round(total_spent, 2)
            }
            
        except Exception as e:
            return False, {}
    
    def get_instructor_analytics(self, instructor_id):
        """Get comprehensive analytics for an instructor"""
        try:
            # Total courses
            total_courses = self.db['courses'].count_documents({
                'instructor_id': ObjectId(instructor_id)
            })
            
            # Get course IDs
            courses = list(self.db['courses'].find(
                {'instructor_id': ObjectId(instructor_id)},
                {'_id': 1}
            ))
            course_ids = [str(c['_id']) for c in courses]  # Convert to strings
            
            # Total students (enrollments)
            total_students = self.db['enrollments'].count_documents({
                'course_id': {'$in': course_ids}
            })
            
            # Active students
            active_students = self.db['enrollments'].count_documents({
                'course_id': {'$in': course_ids},
                'status': 'active'
            })
            
            # Revenue
            pipeline_revenue = [
                {'$match': {'course_id': {'$in': course_ids}, 'status': 'completed'}},
                {'$group': {
                    '_id': None,
                    'total_revenue': {'$sum': '$amount'}
                }}
            ]
            revenue_result = list(self.db['payments'].aggregate(pipeline_revenue))
            total_revenue = revenue_result[0]['total_revenue'] if revenue_result else 0
            
            # Average rating - aggregate from courses directly
            pipeline_rating = [
                {'$match': {'instructor_id': ObjectId(instructor_id)}},
                {'$group': {
                    '_id': None,
                    'avg_rating': {'$avg': '$rating'}
                }}
            ]
            rating_result = list(self.db['courses'].aggregate(pipeline_rating))
            avg_rating = rating_result[0]['avg_rating'] if rating_result else 0
            
            # Exams created
            exams_created = self.db['exams'].count_documents({
                'instructor_id': ObjectId(instructor_id)
            })
            
            # Live classes scheduled
            live_classes = self.db['live_classes'].count_documents({
                'instructor_id': ObjectId(instructor_id)
            })
            
            return True, {
                'total_courses': total_courses,
                'total_students': total_students,
                'active_students': active_students,
                'total_revenue': round(total_revenue, 2),
                'average_rating': round(avg_rating, 2),
                'exams_created': exams_created,
                'live_classes_scheduled': live_classes
            }
            
        except Exception as e:
            return False, {}
    
    def get_admin_analytics(self):
        """Get comprehensive analytics for admin dashboard"""
        try:
            # Total users
            total_students = self.db['users'].count_documents({'role': 'student'})
            total_instructors = self.db['users'].count_documents({'role': 'instructor'})
            total_admins = self.db['users'].count_documents({'role': 'admin'})
            
            # Total courses
            total_courses = self.db['courses'].count_documents({})
            active_courses = self.db['courses'].count_documents({'status': 'published'})
            
            # Enrollments
            total_enrollments = self.db['enrollments'].count_documents({})
            active_enrollments = self.db['enrollments'].count_documents({'status': 'active'})
            
            # Revenue
            pipeline_revenue = [
                {'$match': {'status': 'completed'}},
                {'$group': {
                    '_id': None,
                    'total_revenue': {'$sum': '$amount'},
                    'total_transactions': {'$sum': 1}
                }}
            ]
            revenue_result = list(self.db['payments'].aggregate(pipeline_revenue))
            total_revenue = revenue_result[0]['total_revenue'] if revenue_result else 0
            total_transactions = revenue_result[0]['total_transactions'] if revenue_result else 0
            
            # Certificates
            total_certificates = self.db['certificates'].count_documents({'status': 'active'})
            pending_approvals = self.db['exam_submissions'].count_documents({
                'passed': True,
                'graded': True,
                'certificate_generated': False
            })
            
            # Exams
            total_exams = self.db['exams'].count_documents({})
            submissions = self.db['exam_submissions'].count_documents({})
            
            # Live classes
            total_live_classes = self.db['live_classes'].count_documents({})
            upcoming_classes = self.db['live_classes'].count_documents({
                'scheduled_at': {'$gte': datetime.now()}
            })
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            new_students = self.db['users'].count_documents({
                'role': 'student',
                'created_at': {'$gte': thirty_days_ago}
            })
            
            new_enrollments = self.db['enrollments'].count_documents({
                'enrolled_at': {'$gte': thirty_days_ago}
            })
            
            # Revenue trend (last 7 days)
            revenue_trend = []
            for i in range(6, -1, -1):
                day = datetime.now() - timedelta(days=i)
                day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
                day_end = day_start + timedelta(days=1)
                
                daily_revenue = list(self.db['payments'].aggregate([
                    {
                        '$match': {
                            'status': 'completed',
                            'paid_at': {'$gte': day_start, '$lt': day_end}
                        }
                    },
                    {
                        '$group': {
                            '_id': None,
                            'revenue': {'$sum': '$amount'}
                        }
                    }
                ]))
                
                revenue_trend.append({
                    'date': day.strftime('%Y-%m-%d'),
                    'revenue': daily_revenue[0]['revenue'] if daily_revenue else 0
                })
            
            return True, {
                'users': {
                    'total_students': total_students,
                    'total_instructors': total_instructors,
                    'total_admins': total_admins,
                    'new_students_30_days': new_students
                },
                'courses': {
                    'total_courses': total_courses,
                    'active_courses': active_courses
                },
                'enrollments': {
                    'total_enrollments': total_enrollments,
                    'active_enrollments': active_enrollments,
                    'new_enrollments_30_days': new_enrollments
                },
                'revenue': {
                    'total_revenue': round(total_revenue, 2),
                    'total_transactions': total_transactions,
                    'revenue_trend': revenue_trend
                },
                'certificates': {
                    'total_issued': total_certificates,
                    'pending_approvals': pending_approvals
                },
                'exams': {
                    'total_exams': total_exams,
                    'total_submissions': submissions
                },
                'live_classes': {
                    'total_scheduled': total_live_classes,
                    'upcoming': upcoming_classes
                }
            }
            
        except Exception as e:
            return False, {}
    
    def get_course_performance(self, course_id):
        """Get detailed performance metrics for a specific course"""
        try:
            # Enrollments
            enrollments = self.db['enrollments'].count_documents({
                'course_id': ObjectId(course_id)
            })
            
            # Completion rate
            completed = self.db['enrollments'].count_documents({
                'course_id': ObjectId(course_id),
                'completed': True
            })
            completion_rate = (completed / enrollments * 100) if enrollments > 0 else 0
            
            # Average progress
            pipeline_progress = [
                {'$match': {'course_id': ObjectId(course_id)}},
                {'$group': {
                    '_id': None,
                    'avg_progress': {'$avg': '$progress'}
                }}
            ]
            progress_result = list(self.db['enrollments'].aggregate(pipeline_progress))
            avg_progress = progress_result[0]['avg_progress'] if progress_result else 0
            
            # Exam statistics
            exam_ids = [e['_id'] for e in self.db['exams'].find({'course_id': ObjectId(course_id)}, {'_id': 1})]
            
            total_submissions = self.db['exam_submissions'].count_documents({
                'course_id': ObjectId(course_id)
            })
            
            passed_submissions = self.db['exam_submissions'].count_documents({
                'course_id': ObjectId(course_id),
                'passed': True
            })
            
            pass_rate = (passed_submissions / total_submissions * 100) if total_submissions > 0 else 0
            
            # Revenue
            pipeline_revenue = [
                {'$match': {'course_id': ObjectId(course_id), 'status': 'completed'}},
                {'$group': {
                    '_id': None,
                    'total_revenue': {'$sum': '$amount'}
                }}
            ]
            revenue_result = list(self.db['payments'].aggregate(pipeline_revenue))
            total_revenue = revenue_result[0]['total_revenue'] if revenue_result else 0
            
            return True, {
                'enrollments': enrollments,
                'completed': completed,
                'completion_rate': round(completion_rate, 2),
                'average_progress': round(avg_progress, 2),
                'total_submissions': total_submissions,
                'passed_submissions': passed_submissions,
                'pass_rate': round(pass_rate, 2),
                'total_revenue': round(total_revenue, 2)
            }
            
        except Exception as e:
            return False, {}
