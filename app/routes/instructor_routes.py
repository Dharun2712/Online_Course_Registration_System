"""
Instructor Routes
Handles instructor-specific operations
"""
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import role_required, get_current_user
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.exam_service import ExamService
from app.services.certificate_service import CertificateService
from app.services.liveclass_service import LiveClassService
from app.services.attendance_service import AttendanceService
from app.services.analytics_service import AnalyticsService
from datetime import datetime

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/courses', methods=['GET'])
@role_required('instructor')
def get_my_courses():
    """Get all courses created by instructor"""
    current_user = get_current_user()
    
    course_service = CourseService(current_app.db)
    courses = course_service.get_instructor_courses(current_user['user_id'])
    
    return jsonify({
        'success': True,
        'courses': courses
    }), 200

@instructor_bp.route('/courses', methods=['POST'])
@role_required('instructor')
def create_course():
    """Create a new course"""
    current_user = get_current_user()
    data = request.get_json()
    # Ensure DB connection is available
    if getattr(current_app, 'db', None) is None:
        return jsonify({'success': False, 'message': 'Database not connected. Please ensure MongoDB is running and MONGO_URI is configured.'}), 503
    
    course_service = CourseService(current_app.db)
    
    # Build course data with all fields
    course_data = {
        'title': data.get('title'),
        'description': data.get('description'),
        'price': data.get('price', 0),
        'duration': data.get('duration', ''),
        'level': data.get('level', 'Beginner'),
        'tags': data.get('tags', []),
        'thumbnail': data.get('thumbnail', '')
    }
    
    success, message, course_id = course_service.create_course(
        instructor_id=current_user['user_id'],
        course_data=course_data
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': message,
            'course_id': course_id
        }), 201
    else:
        # Return 'message' key so frontend can display the error text consistently
        return jsonify({'success': False, 'message': message}), 400

@instructor_bp.route('/courses/<course_id>', methods=['PUT'])
@role_required('instructor')
def update_course(course_id):
    """Update course details"""
    current_user = get_current_user()
    data = request.get_json()
    
    course_service = CourseService(current_app.db)
    
    success, message = course_service.update_course(
        course_id=course_id,
        instructor_id=current_user['user_id'],
        updates=data
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@instructor_bp.route('/courses/<course_id>/publish', methods=['POST'])
@role_required('instructor')
def publish_course(course_id):
    """Publish a course"""
    current_user = get_current_user()
    
    course_service = CourseService(current_app.db)
    
    success, message = course_service.publish_course(course_id, current_user['user_id'])
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@instructor_bp.route('/courses/<course_id>/materials', methods=['POST'])
@role_required('instructor')
def add_material(course_id):
    """Add learning material to course (file or link)"""
    current_user = get_current_user()
    
    # Check if it's a file upload or JSON data
    if request.content_type and 'multipart/form-data' in request.content_type:
        # File upload
        file = request.files.get('file')
        title = request.form.get('title', 'Untitled Material')
        description = request.form.get('description', '')
        
        if not file:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        # Save file (basic implementation - should use cloud storage in production)
        import os
        from werkzeug.utils import secure_filename
        
        upload_folder = os.path.join('static', 'uploads', 'materials')
        os.makedirs(upload_folder, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, f"{course_id}_{filename}")
        file.save(file_path)
        
        material_data = {
            'title': title,
            'description': description,
            'filename': filename,
            'file_url': f'/static/uploads/materials/{course_id}_{filename}',
            'type': 'file'
        }
    else:
        # Link/JSON data
        data = request.get_json()
        material_data = {
            'title': data.get('title', 'Untitled'),
            'description': data.get('description', ''),
            'url': data.get('url', ''),
            'type': data.get('type', 'link')
        }
    
    # Save to database
    try:
        from datetime import datetime
        db = current_app.db
        material_data['course_id'] = course_id
        material_data['instructor_id'] = current_user['user_id']
        material_data['created_at'] = datetime.utcnow()
        
        result = db.materials.insert_one(material_data)
        
        return jsonify({
            'success': True,
            'message': 'Material added successfully',
            'material_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@instructor_bp.route('/courses/<course_id>/students', methods=['GET'])
@role_required('instructor')
def get_course_students(course_id):
    """Get all students enrolled in a course"""
    current_user = get_current_user()
    
    # Verify instructor owns this course
    course_service = CourseService(current_app.db)
    course = course_service.get_course(course_id)
    
    if not course or course['instructor_id'] != current_user['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    enrollment_service = EnrollmentService(current_app.db)
    students = enrollment_service.get_course_students(course_id)
    
    return jsonify({
        'success': True,
        'students': students
    }), 200

@instructor_bp.route('/courses/<course_id>/students/<student_id>/videos', methods=['GET'])
@role_required('instructor')
def get_student_video_progress(course_id, student_id):
    """Get detailed video completion progress for a student"""
    current_user = get_current_user()
    
    # Verify instructor owns this course
    course_service = CourseService(current_app.db)
    course = course_service.get_course(course_id)
    
    if not course or course['instructor_id'] != current_user['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        from bson import ObjectId
        
        # Get all completed videos for this student in this course
        completed_videos = list(current_app.db.video_progress.find({
            'student_id': ObjectId(student_id),
            'course_id': ObjectId(course_id),
            'completed': True
        }).sort('completed_at', -1))
        
        # Convert ObjectIds to strings
        for video in completed_videos:
            video['_id'] = str(video['_id'])
            video['student_id'] = str(video['student_id'])
            video['course_id'] = str(video['course_id'])
        
        return jsonify({
            'success': True,
            'completed_videos': completed_videos,
            'total_completed': len(completed_videos)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch video progress: {str(e)}'
        }), 400

@instructor_bp.route('/statistics', methods=['GET'])
@role_required('instructor')
def get_statistics():
    """Get instructor statistics"""
    current_user = get_current_user()
    
    course_service = CourseService(current_app.db)
    stats = course_service.get_course_statistics(instructor_id=current_user['user_id'])
    
    return jsonify({
        'success': True,
        'statistics': stats
    }), 200

@instructor_bp.route('/dashboard', methods=['GET'])
@role_required('instructor')
def get_dashboard_data():
    """Get comprehensive dashboard data"""
    current_user = get_current_user()
    
    course_service = CourseService(current_app.db)
    analytics_service = AnalyticsService(current_app.db)
    enrollment_service = EnrollmentService(current_app.db)
    
    # Get all courses
    courses = course_service.get_instructor_courses(current_user['user_id'])
    
    # Add enrolled_count to each course
    for course in courses:
        course_enrollments = current_app.db.enrollments.count_documents({
            'course_id': str(course['_id']),
            'status': 'active'
        })
        course['enrolled_count'] = course_enrollments
    
    # Get comprehensive analytics
    success, analytics = analytics_service.get_instructor_analytics(current_user['user_id'])
    
    # Get recent enrollments across all courses
    recent_enrollments = []
    
    for course in courses[:5]:  # Get enrollments for top 5 courses
        course_enrollments = enrollment_service.get_course_students(course['_id'])
        recent_enrollments.extend(course_enrollments[:3])  # Top 3 from each
    
    return jsonify({
        'success': True,
        'courses': courses,
        'analytics': analytics if success else {},
        'recent_enrollments': recent_enrollments[:10]  # Limit to 10
    }), 200

# Exam Management Routes
@instructor_bp.route('/exams', methods=['POST'])
@role_required('instructor')
def create_exam():
    """Create a new exam for a course"""
    current_user = get_current_user()
    data = request.get_json()
    
    exam_service = ExamService(current_app.db)
    success, result = exam_service.create_exam(
        data.get('course_id'),
        current_user['user_id'],
        data
    )
    
    if success:
        return jsonify({'success': True, 'exam_id': result}), 201
    else:
        return jsonify({'success': False, 'error': result}), 400

@instructor_bp.route('/courses/<course_id>/exams', methods=['GET'])
@role_required('instructor')
def get_course_exams(course_id):
    """Get all exams for a course"""
    exam_service = ExamService(current_app.db)
    success, exams = exam_service.get_course_exams(course_id, include_questions=False)
    
    return jsonify({'success': success, 'exams': exams}), 200

@instructor_bp.route('/liveclasses', methods=['POST'])
@role_required('instructor')
def schedule_live_class_legacy():
    """Schedule a new live class for a course"""
    current_user = get_current_user()
    data = request.get_json()

    live_service = LiveClassService(current_app.db)
    success, result = live_service.schedule_live_class(data.get('course_id'), current_user['user_id'], data)

    if success:
        return jsonify({'success': True, 'liveclass_id': result}), 201
    else:
        return jsonify({'success': False, 'error': result}), 400
@instructor_bp.route('/exams/<exam_id>/submissions', methods=['GET'])
@role_required('instructor')
def get_exam_submissions(exam_id):
    """Get all submissions for an exam"""
    exam_service = ExamService(current_app.db)
    success, submissions = exam_service.get_exam_submissions(exam_id)
    
    return jsonify({'success': success, 'submissions': submissions}), 200

@instructor_bp.route('/submissions/<submission_id>/grade', methods=['POST'])
@role_required('instructor')
def grade_submission(submission_id):
    """Grade subjective answers in a submission"""
    data = request.get_json()
    
    exam_service = ExamService(current_app.db)
    success, result = exam_service.grade_subjective_answers(
        submission_id,
        data.get('graded_answers', [])
    )
    
    if success:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False, 'error': result}), 400

@instructor_bp.route('/submissions/<submission_id>/certificate', methods=['POST'])
@role_required('instructor')
def generate_certificate(submission_id):
    """Generate certificate for a passed student"""
    current_user = get_current_user()
    
    cert_service = CertificateService(current_app.db)
    success, result = cert_service.generate_certificate(
        submission_id,
        current_user['user_id']
    )
    
    if success:
        return jsonify({'success': True, 'certificate': result}), 201
    else:
        return jsonify({'success': False, 'error': result}), 400

# Live Class Routes
@instructor_bp.route('/live-classes', methods=['POST'])
@role_required('instructor')
def schedule_live_class():
    """Schedule a new live class"""
    current_user = get_current_user()
    data = request.get_json()
    
    liveclass_service = LiveClassService(current_app.db)
    success, result = liveclass_service.schedule_live_class(
        data.get('course_id'),
        current_user['user_id'],
        data
    )
    
    if success:
        return jsonify({'success': True, 'class_id': result}), 201
    else:
        return jsonify({'success': False, 'error': result}), 400

@instructor_bp.route('/live-classes', methods=['GET'])
@role_required('instructor')
def get_my_live_classes():
    """Get instructor's live classes"""
    current_user = get_current_user()
    
    liveclass_service = LiveClassService(current_app.db)
    success, classes = liveclass_service.get_upcoming_classes(current_user['user_id'], 'instructor')
    
    return jsonify({'success': success, 'live_classes': classes}), 200

@instructor_bp.route('/live-classes/<class_id>', methods=['PUT'])
@role_required('instructor')
def update_live_class(class_id):
    """Update live class details"""
    data = request.get_json()
    
    liveclass_service = LiveClassService(current_app.db)
    success, message = liveclass_service.update_live_class(class_id, data)
    
    return jsonify({'success': success, 'message': message}), 200 if success else 400

@instructor_bp.route('/live-classes/<class_id>', methods=['DELETE'])
@role_required('instructor')
def delete_live_class(class_id):
    """Delete a live class"""
    liveclass_service = LiveClassService(current_app.db)
    success, message = liveclass_service.delete_live_class(class_id)
    
    return jsonify({'success': success, 'message': message}), 200 if success else 404

@instructor_bp.route('/live-classes/<class_id>/attendees', methods=['GET'])
@role_required('instructor')
def get_live_class_attendees(class_id):
    """Get attendees for a live class"""
    liveclass_service = LiveClassService(current_app.db)
    success, attendees = liveclass_service.get_class_attendees(class_id)
    
    return jsonify({'success': success, 'attendees': attendees}), 200

# Student Reports and Analytics
@instructor_bp.route('/students/<student_id>/report', methods=['GET'])
@role_required('instructor')
def get_student_report(student_id):
    """Get detailed report for a specific student"""
    course_id = request.args.get('course_id')
    
    analytics_service = AnalyticsService(current_app.db)
    success, student_analytics = analytics_service.get_student_analytics(student_id)
    
    # Get exam submissions
    exam_service = ExamService(current_app.db)
    _, submissions = exam_service.get_student_submissions(student_id, course_id)
    
    # Get attendance
    attendance_service = AttendanceService(current_app.db)
    _, attendance_records = attendance_service.get_student_attendance(student_id, course_id)
    _, attendance_stats = attendance_service.get_attendance_statistics(student_id, course_id)
    
    return jsonify({
        'success': True,
        'analytics': student_analytics if success else {},
        'submissions': submissions,
        'attendance_records': attendance_records,
        'attendance_stats': attendance_stats
    }), 200

@instructor_bp.route('/courses/<course_id>/attendance-report', methods=['GET'])
@role_required('instructor')
def get_course_attendance_report(course_id):
    """Get attendance report for all students in a course"""
    attendance_service = AttendanceService(current_app.db)
    success, report = attendance_service.get_course_attendance_report(course_id)
    
    return jsonify({'success': success, 'report': report}), 200

@instructor_bp.route('/courses/<course_id>/performance', methods=['GET'])
@role_required('instructor')
def get_course_performance(course_id):
    """Get detailed performance metrics for a course"""
    analytics_service = AnalyticsService(current_app.db)
    success, performance = analytics_service.get_course_performance(course_id)
    
    return jsonify({'success': success, 'performance': performance}), 200

