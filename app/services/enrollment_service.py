"""
Enrollment Service
Business logic for course enrollments
"""
from app.models.enrollment_model import Enrollment
from app.models.course_model import Course
from app.models.user_model import User
from app.models.payment_model import Payment
from app.utils.logger import log_error, log_info

class EnrollmentService:
    def __init__(self, db):
        self.enrollment_model = Enrollment(db)
        self.course_model = Course(db)
        self.user_model = User(db)
        self.payment_model = Payment(db)
    
    def enroll_student(self, student_id, course_id, payment_id=None):
        """Enroll student in a course"""
        try:
            # Check if course exists
            course = self.course_model.find_by_id(course_id)
            if not course:
                return False, "Course not found"
            
            if not course.get('is_published'):
                return False, "Course is not published"
            
            # Check if already enrolled
            if self.enrollment_model.is_enrolled(student_id, course_id):
                return False, "Already enrolled in this course"
            
            # Check if payment required
            if course['price'] > 0 and not payment_id:
                return False, "Payment required for this course"
            
            # Create enrollment
            enrollment_id = self.enrollment_model.enroll(student_id, course_id, payment_id)
            
            if not enrollment_id:
                return False, "Enrollment failed"
            
            # Update course enrollment count
            self.course_model.enroll_student(course_id, student_id)
            
            # Update user's enrolled courses
            self.user_model.add_enrolled_course(student_id, course_id)
            
            log_info(f"Student {student_id} enrolled in course {course_id}")
            return True, "Enrollment successful"
        
        except Exception as e:
            log_error(str(e), "enrollment_service.enroll_student")
            return False, "Enrollment failed"
    
    def get_student_enrollments(self, student_id, status=None):
        """Get all enrollments for a student"""
        try:
            enrollments = self.enrollment_model.get_student_enrollments(student_id, status)
            
            # Enrich with course details
            for enrollment in enrollments:
                course = self.course_model.find_by_id(enrollment['course_id'])
                enrollment['course'] = course
            
            return enrollments
        except Exception as e:
            log_error(str(e), "enrollment_service.get_student_enrollments")
            return []
    
    def get_course_students(self, course_id):
        """Get all students enrolled in a course"""
        try:
            enrollments = self.enrollment_model.get_course_enrollments(course_id)
            
            # Enrich with student details
            for enrollment in enrollments:
                student = self.user_model.find_by_id(enrollment['student_id'])
                enrollment['student'] = student
            
            return enrollments
        except Exception as e:
            log_error(str(e), "enrollment_service.get_course_students")
            return []
    
    def update_progress(self, student_id, course_id, progress_percent):
        """Update student progress"""
        try:
            success = self.enrollment_model.update_progress(
                student_id, course_id, progress_percent
            )
            
            if success:
                # Check if certificate should be issued
                if progress_percent >= 100:
                    self.enrollment_model.issue_certificate(student_id, course_id)
                
                return True, "Progress updated"
            else:
                return False, "Failed to update progress"
        
        except Exception as e:
            log_error(str(e), "enrollment_service.update_progress")
            return False, "Failed to update progress"
    
    def mark_material_completed(self, student_id, course_id, material_id):
        """Mark course material as completed"""
        try:
            success = self.enrollment_model.mark_material_completed(
                student_id, course_id, material_id
            )
            
            if success:
                return True, "Material marked as completed"
            else:
                return False, "Failed to mark material"
        
        except Exception as e:
            log_error(str(e), "enrollment_service.mark_material_completed")
            return False, "Failed to mark material"
    
    def drop_course(self, student_id, course_id):
        """Drop/unenroll from course"""
        try:
            success = self.enrollment_model.drop_course(student_id, course_id)
            
            if success:
                log_info(f"Student {student_id} dropped course {course_id}")
                return True, "Course dropped successfully"
            else:
                return False, "Failed to drop course"
        
        except Exception as e:
            log_error(str(e), "enrollment_service.drop_course")
            return False, "Failed to drop course"
    
    def get_enrollment_statistics(self, student_id=None, course_id=None):
        """Get enrollment statistics"""
        try:
            stats = self.enrollment_model.get_statistics(student_id, course_id)
            return stats
        except Exception as e:
            log_error(str(e), "enrollment_service.get_enrollment_statistics")
            return {}
