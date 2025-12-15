"""
Course Service
Business logic for course management
"""
from app.models.course_model import Course
from app.utils.validators import validate_course_data
from app.utils.logger import log_error, log_info

class CourseService:
    def __init__(self, db):
        self.course_model = Course(db)
    
    def create_course(self, instructor_id, course_data):
        """Create a new course"""
        # Validate course data
        is_valid, message = validate_course_data(course_data)
        if not is_valid:
            return False, message, None
        
        try:
            course_id = self.course_model.create(
                title=course_data['title'],
                description=course_data['description'],
                instructor_id=instructor_id,
                price=course_data.get('price', 0),
                tags=course_data.get('tags', []),
                thumbnail=course_data.get('thumbnail', ''),
                duration=course_data.get('duration', ''),
                level=course_data.get('level', 'Beginner')
            )
            # Auto-approve and publish the course so it is visible on home/student views
            try:
                self.course_model.update(str(course_id), {'status': 'approved', 'is_published': True})
            except Exception:
                pass

            log_info(f"Course created and published: {course_data['title']} by instructor {instructor_id}")
            return True, "Course created and published successfully", str(course_id)
        
        except Exception as e:
            log_error(str(e), "course_service.create_course")
            return False, "Failed to create course", None
    
    def get_course(self, course_id):
        """Get course details"""
        try:
            course = self.course_model.find_by_id(course_id)
            return course
        except Exception as e:
            log_error(str(e), "course_service.get_course")
            return None
    
    def get_all_published_courses(self, page=1, per_page=12):
        """Get all published courses with pagination"""
        try:
            skip = (page - 1) * per_page
            courses = self.course_model.get_published_courses(skip, per_page)
            return courses
        except Exception as e:
            log_error(str(e), "course_service.get_all_published_courses")
            return []
    
    def search_courses(self, query, page=1, per_page=12):
        """Search courses"""
        try:
            skip = (page - 1) * per_page
            courses = self.course_model.search_courses(query, skip, per_page)
            return courses
        except Exception as e:
            log_error(str(e), "course_service.search_courses")
            return []
    
    def get_instructor_courses(self, instructor_id):
        """Get all courses by instructor"""
        try:
            courses = self.course_model.get_courses_by_instructor(instructor_id)
            return courses
        except Exception as e:
            log_error(str(e), "course_service.get_instructor_courses")
            return []
    
    def update_course(self, course_id, instructor_id, updates):
        """Update course (only by owner)"""
        try:
            course = self.course_model.find_by_id(course_id)
            
            if not course:
                return False, "Course not found"
            
            if course['instructor_id'] != str(instructor_id):
                return False, "Unauthorized to update this course"
            
            success = self.course_model.update(course_id, updates)
            
            if success:
                return True, "Course updated successfully"
            else:
                return False, "Failed to update course"
        
        except Exception as e:
            log_error(str(e), "course_service.update_course")
            return False, "Failed to update course"
    
    def publish_course(self, course_id, instructor_id):
        """Publish a course"""
        try:
            course = self.course_model.find_by_id(course_id)
            
            if not course:
                return False, "Course not found"
            
            if course['instructor_id'] != str(instructor_id):
                return False, "Unauthorized"
            
            if course['status'] != 'approved':
                return False, "Course must be approved by admin first"
            
            success = self.course_model.publish_course(course_id)
            
            if success:
                return True, "Course published successfully"
            else:
                return False, "Failed to publish course"
        
        except Exception as e:
            log_error(str(e), "course_service.publish_course")
            return False, "Failed to publish course"
    
    def add_course_material(self, course_id, instructor_id, material_data):
        """Add material to course"""
        try:
            course = self.course_model.find_by_id(course_id)
            
            if not course or course['instructor_id'] != str(instructor_id):
                return False, "Unauthorized"
            
            success = self.course_model.add_material(course_id, material_data)
            
            if success:
                return True, "Material added successfully"
            else:
                return False, "Failed to add material"
        
        except Exception as e:
            log_error(str(e), "course_service.add_course_material")
            return False, "Failed to add material"
    
    def get_course_statistics(self, instructor_id=None):
        """Get course statistics"""
        try:
            stats = self.course_model.get_statistics(instructor_id)
            return stats
        except Exception as e:
            log_error(str(e), "course_service.get_course_statistics")
            return {}
