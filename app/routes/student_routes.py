"""
Student Routes
Handles student-specific operations
"""
from flask import Blueprint, request, jsonify, current_app, send_file
import os
from app.utils.jwt_helper import role_required, get_current_user
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.chatbot_service import chatbot_service
from app.services.recommendation_service import recommendation_service
from app.services.attendance_service import AttendanceService
from app.services.exam_service import ExamService
from app.services.certificate_service import CertificateService
from app.services.certificate_service import CertificateService
from app.services.liveclass_service import LiveClassService
from app.services.payment_service import PaymentService
from app.services.analytics_service import AnalyticsService
from app.models.progress_model import Progress

student_bp = Blueprint('student', __name__)

@student_bp.route('/courses', methods=['GET'])
def browse_courses():
    """Browse all available courses - PUBLIC ENDPOINT"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    search = request.args.get('search', '')
    
    course_service = CourseService(current_app.db)
    
    if search:
        courses = course_service.search_courses(search, page, per_page)
    else:
        courses = course_service.get_all_published_courses(page, per_page)
    
    return jsonify({
        'success': True,
        'courses': courses,
        'page': page,
        'per_page': per_page
    }), 200

@student_bp.route('/courses/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """Get detailed course information - PUBLIC ENDPOINT"""
    course_service = CourseService(current_app.db)
    course = course_service.get_course(course_id)
    
    if course:
        return jsonify({'success': True, 'course': course}), 200
    else:
        return jsonify({'success': False, 'error': 'Course not found'}), 404

@student_bp.route('/enroll', methods=['POST'])
@role_required('student')
def enroll_in_course():
    """Enroll in a course"""
    current_user = get_current_user()
    data = request.get_json()
    
    enrollment_service = EnrollmentService(current_app.db)
    
    success, message = enrollment_service.enroll_student(
        student_id=current_user['user_id'],
        course_id=data.get('course_id'),
        payment_id=data.get('payment_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    else:
        return jsonify({'success': False, 'error': message}), 400

@student_bp.route('/my-courses', methods=['GET'])
@role_required('student')
def get_my_courses():
    """Get student's enrolled courses"""
    current_user = get_current_user()
    status = request.args.get('status')
    
    enrollment_service = EnrollmentService(current_app.db)
    enrollments = enrollment_service.get_student_enrollments(current_user['user_id'], status)
    
    return jsonify({
        'success': True,
        'enrollments': enrollments
    }), 200

@student_bp.route('/enrollments', methods=['GET'])
@role_required('student')
def get_enrollments():
    """Get student's enrolled courses (alias for my-courses)"""
    current_user = get_current_user()
    status = request.args.get('status')
    
    enrollment_service = EnrollmentService(current_app.db)
    enrollments = enrollment_service.get_student_enrollments(current_user['user_id'], status)
    
    return jsonify({
        'success': True,
        'enrollments': enrollments
    }), 200

@student_bp.route('/progress/<course_id>', methods=['POST'])
@role_required('student')
def update_progress(course_id):
    """Update progress in a course"""
    current_user = get_current_user()
    data = request.get_json()
    
    enrollment_service = EnrollmentService(current_app.db)
    
    success, message = enrollment_service.update_progress(
        student_id=current_user['user_id'],
        course_id=course_id,
        progress_percent=data.get('progress_percent', 0)
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@student_bp.route('/complete-material', methods=['POST'])
@role_required('student')
def complete_material():
    """Mark a course material as completed"""
    current_user = get_current_user()
    data = request.get_json()
    
    enrollment_service = EnrollmentService(current_app.db)
    
    success, message = enrollment_service.mark_material_completed(
        student_id=current_user['user_id'],
        course_id=data.get('course_id'),
        material_id=data.get('material_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@student_bp.route('/drop-course/<course_id>', methods=['POST'])
@role_required('student')
def drop_course(course_id):
    """Drop/unenroll from a course"""
    current_user = get_current_user()
    
    enrollment_service = EnrollmentService(current_app.db)
    success, message = enrollment_service.drop_course(current_user['user_id'], course_id)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400

@student_bp.route('/chatbot', methods=['POST'])
@role_required('student')
def chatbot():
    """AI chatbot for course assistance"""
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context')
    
    response = chatbot_service.get_response(message, context)
    
    return jsonify({
        'success': True,
        'response': response
    }), 200

@student_bp.route('/recommendations', methods=['GET'])
@role_required('student')
def get_recommendations():
    """Get AI-powered course recommendations based on enrollment history"""
    current_user = get_current_user()
    
    course_service = CourseService(current_app.db)
    enrollment_service = EnrollmentService(current_app.db)
    
    # Get enrolled courses
    enrollments = enrollment_service.get_student_enrollments(current_user['user_id'])
    enrolled_course_ids = [e.get('course_id') for e in enrollments if 'course_id' in e]
    
    enrolled_courses = []
    for course_id in enrolled_course_ids:
        course = course_service.get_course(course_id)
        if course:
            enrolled_courses.append(course)
    
    # Get all available courses
    all_courses = course_service.get_all_published_courses(1, 50)
    
    # Get recommendations based on enrollment history
    recommendations = recommendation_service.get_enrollment_based_recommendations(
        enrolled_courses,
        all_courses,
        count=5
    )
    
    return jsonify({
        'success': True,
        'recommendations': recommendations
    }), 200

@student_bp.route('/analytics', methods=['GET'])
@role_required('student')
def get_analytics():
    """Get student learning analytics"""
    current_user = get_current_user()
    
    analytics_service = AnalyticsService(current_app.db)
    success, analytics = analytics_service.get_student_analytics(current_user['user_id'])
    
    if success:
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch analytics'}), 500

# Attendance Routes
@student_bp.route('/attendance', methods=['GET'])
@role_required('student')
def get_attendance():
    """Get student attendance records"""
    current_user = get_current_user()
    course_id = request.args.get('course_id')
    
    attendance_service = AttendanceService(current_app.db)
    success, records = attendance_service.get_student_attendance(current_user['user_id'], course_id)
    
    if success:
        success_stats, stats = attendance_service.get_attendance_statistics(current_user['user_id'], course_id)
        return jsonify({
            'success': True,
            'records': records,
            'statistics': stats if success_stats else {}
        }), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch attendance'}), 500

@student_bp.route('/attendance/mark', methods=['POST'])
@role_required('student')
def mark_attendance():
    """Mark attendance (automatic on login or manual for live class)"""
    current_user = get_current_user()
    data = request.get_json()
    
    attendance_service = AttendanceService(current_app.db)
    
    if data.get('type') == 'live_class':
        success, message = attendance_service.mark_live_class_attendance(
            current_user['user_id'],
            data.get('live_class_id'),
            data.get('course_id')
        )
    else:
        success, message = attendance_service.mark_daily_login(current_user['user_id'])
    
    return jsonify({'success': success, 'message': message}), 200 if success else 400

@student_bp.route('/courses/<course_id>/attendance', methods=['POST'])
@role_required('student')
def mark_course_attendance(course_id):
    """Mark attendance for a specific course"""
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        from datetime import datetime
        from bson import ObjectId
        
        # Check if already marked for today
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        existing = current_app.db.attendance.find_one({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'date': {'$gte': today}
        })
        
        if existing:
            return jsonify({
                'success': True,
                'message': 'Attendance already marked for today',
                'already_marked': True
            }), 200
        
        # Mark new attendance
        attendance_data = {
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'date': datetime.now(),
            'status': data.get('status', 'present'),
            'marked_at': datetime.now()
        }
        
        result = current_app.db.attendance.insert_one(attendance_data)
        
        return jsonify({
            'success': True,
            'message': 'Attendance marked successfully',
            'attendance_id': str(result.inserted_id)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to mark attendance: {str(e)}'
        }), 400

# Video Completion Tracking
@student_bp.route('/courses/<course_id>/videos/<video_id>/complete', methods=['POST'])
@role_required('student')
def mark_video_complete(course_id, video_id):
    """Mark a video module as completed and update progress"""
    current_user = get_current_user()
    data = request.get_json()
    
    try:
        from datetime import datetime
        from bson import ObjectId
        
        # Get total number of videos for the course (default 15 from playlist)
        total_videos = data.get('total_videos', 15)
        
        # Check if video already marked as complete
        existing = current_app.db.video_progress.find_one({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'video_id': video_id
        })
        
        if not existing:
            # Create new video completion record
            video_progress = {
                'student_id': ObjectId(current_user['user_id']),
                'course_id': ObjectId(course_id),
                'video_id': video_id,
                'video_index': data.get('video_index', 0),
                'video_title': data.get('video_title', ''),
                'completed': True,
                'completed_at': datetime.now(),
                'watch_time': data.get('watch_time', 0)  # in seconds
            }
            
            current_app.db.video_progress.insert_one(video_progress)
        
        # Calculate overall progress based on completed videos
        completed_count = current_app.db.video_progress.count_documents({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'completed': True
        })
        
        progress_percentage = round((completed_count / total_videos) * 100, 2)
        
        # Update enrollment progress
        enrollment_service = EnrollmentService(current_app.db)
        enrollment_service.update_progress(
            current_user['user_id'], 
            course_id, 
            progress_percentage
        )
        
        # Mark material as completed in enrollment
        enrollment_service.mark_material_completed(
            current_user['user_id'],
            course_id,
            video_id
        )
        
        return jsonify({
            'success': True,
            'message': 'Video marked as complete',
            'progress': progress_percentage,
            'completed_videos': completed_count,
            'total_videos': total_videos
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to mark video complete: {str(e)}'
        }), 400

@student_bp.route('/courses/<course_id>/videos/progress', methods=['GET'])
@role_required('student')
def get_video_progress(course_id):
    """Get video completion progress for a course"""
    current_user = get_current_user()
    
    try:
        from bson import ObjectId
        
        # Get all completed videos
        completed_videos = list(current_app.db.video_progress.find({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'completed': True
        }))
        
        # Convert ObjectId to string
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

# Exam Routes
@student_bp.route('/courses/<course_id>/exams', methods=['GET'])
@role_required('student')
def get_course_exams_for_student(course_id):
    """Get all exams for a specific course"""
    exam_service = ExamService(current_app.db)
    success, exams = exam_service.get_course_exams(course_id, include_questions=False)
    
    return jsonify({'success': success, 'exams': exams if success else []}), 200

@student_bp.route('/exams', methods=['GET'])
@role_required('student')
def get_student_exams():
    """Get all exams for enrolled courses"""
    current_user = get_current_user()
    course_id = request.args.get('course_id')
    
    exam_service = ExamService(current_app.db)
    
    if course_id:
        success, exams = exam_service.get_course_exams(course_id, include_questions=False)
    else:
        # Get all exams for enrolled courses
        enrollment_service = EnrollmentService(current_app.db)
        enrollments = enrollment_service.get_student_enrollments(current_user['user_id'])
        course_ids = [e.get('course_id') for e in enrollments if 'course_id' in e]
        
        all_exams = []
        for cid in course_ids:
            success, exams = exam_service.get_course_exams(cid, include_questions=False)
            if success:
                all_exams.extend(exams)
        exams = all_exams
        success = True
    
    return jsonify({'success': success, 'exams': exams}), 200

@student_bp.route('/exams/<exam_id>', methods=['GET'])
@role_required('student')
def get_exam_details(exam_id):
    """Get exam details with questions"""
    exam_service = ExamService(current_app.db)
    success, exam = exam_service.get_exam(exam_id)
    
    if success:
        return jsonify({'success': True, 'exam': exam}), 200
    else:
        return jsonify({'success': False, 'error': 'Exam not found'}), 404

@student_bp.route('/exams/<exam_id>/submit', methods=['POST'])
@role_required('student')
def submit_exam(exam_id):
    """Submit exam answers"""
    current_user = get_current_user()
    data = request.get_json()
    
    exam_service = ExamService(current_app.db)
    success, result = exam_service.submit_exam(
        exam_id,
        current_user['user_id'],
        data.get('answers', {})
    )
    
    if success:
        return jsonify({'success': True, 'result': result}), 200
    else:
        return jsonify({'success': False, 'error': result}), 400

@student_bp.route('/submissions', methods=['GET'])
@role_required('student')
def get_student_submissions():
    """Get all exam submissions for current student"""
    current_user = get_current_user()
    
    exam_service = ExamService(current_app.db)
    success, submissions = exam_service.get_student_submissions(current_user['user_id'])
    
    return jsonify({'success': success, 'submissions': submissions}), 200

@student_bp.route('/submissions/<submission_id>', methods=['GET'])
@role_required('student')
def get_submission_details(submission_id):
    """Get details of a specific submission"""
    current_user = get_current_user()
    
    exam_service = ExamService(current_app.db)
    success, submission = exam_service.get_submission(submission_id)
    
    if success and submission and str(submission.get('student_id')) == current_user['user_id']:
        return jsonify({'success': True, 'submission': submission}), 200
    else:
        return jsonify({'success': False, 'error': 'Submission not found'}), 404

@student_bp.route('/certificates', methods=['GET'])
@role_required('student')
def get_student_certificates():
    """Get all certificates for current student"""
    current_user = get_current_user()
    
    cert_service = CertificateService(current_app.db)
    success, certificates = cert_service.get_student_certificates(current_user['user_id'])
    
    return jsonify({'success': success, 'certificates': certificates}), 200

# Certificate Routes
@student_bp.route('/certificates', methods=['GET'])
@role_required('student')
def get_certificates():
    """Get student's certificates"""
    current_user = get_current_user()
    
    certificate_service = CertificateService(current_app.db)
    success, certificates = certificate_service.get_student_certificates(current_user['user_id'])
    
    return jsonify({'success': success, 'certificates': certificates}), 200

@student_bp.route('/certificates/<certificate_id>', methods=['GET'])
@role_required('student')
def get_certificate(certificate_id):
    """Get specific certificate"""
    certificate_service = CertificateService(current_app.db)
    success, certificate = certificate_service.get_certificate(certificate_id)
    
    if success:
        return jsonify({'success': True, 'certificate': certificate}), 200
    else:
        return jsonify({'success': False, 'error': 'Certificate not found'}), 404


@student_bp.route('/certificates/<certificate_id>/download', methods=['GET'])
@role_required('student')
def download_certificate(certificate_id):
    """Download certificate PDF"""
    certificate_service = CertificateService(current_app.db)
    success, certificate = certificate_service.get_certificate(certificate_id)

    if not success:
        return jsonify({'success': False, 'error': 'Certificate not found'}), 404

    file_path = certificate.get('file_path') or certificate.get('certificate_path')
    if not file_path or not os.path.exists(file_path):
        # Attempt to render/generate PDF on demand
        cert_service = CertificateService(current_app.db)
        success_render, result = cert_service.render_certificate_pdf(certificate_id)
        if not success_render:
            return jsonify({'success': False, 'error': 'Certificate file not available and rendering failed'}), 404
        file_path = result

    try:
        return send_file(file_path, as_attachment=True, download_name=f"{certificate.get('certificate_id')}.pdf", mimetype='application/pdf')
    except Exception as e:
        current_app.logger.error(f"Error sending certificate file: {e}")
        return jsonify({'success': False, 'error': 'Failed to send certificate file'}), 500

@student_bp.route('/courses/<course_id>/certificate', methods=['GET'])
@role_required('student')
def get_course_certificate(course_id):
    """Get or generate certificate for a specific course"""
    current_user = get_current_user()
    certificate_service = CertificateService(current_app.db)
    
    try:
        # Check if certificate already exists
        from bson import ObjectId
        certificate = current_app.db.certificates.find_one({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id)
        })
        
        if certificate:
            # Certificate exists, try to send it
            file_path = certificate.get('file_path') or certificate.get('certificate_path')
            if file_path and os.path.exists(file_path):
                return send_file(file_path, as_attachment=True, 
                               download_name=f"certificate_{course_id}.pdf", 
                               mimetype='application/pdf')
        
        # Check if student completed the course
        enrollment = current_app.db.enrollments.find_one({
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id)
        })
        
        if not enrollment or enrollment.get('progress', 0) < 100:
            return jsonify({
                'success': False,
                'error': 'Course not completed yet',
                'progress': enrollment.get('progress', 0) if enrollment else 0
            }), 400
        
        # Generate new certificate
        from datetime import datetime
        cert_data = {
            'student_id': ObjectId(current_user['user_id']),
            'course_id': ObjectId(course_id),
            'issue_date': datetime.now(),
            'status': 'issued'
        }
        result = current_app.db.certificates.insert_one(cert_data)
        
        return jsonify({
            'success': True,
            'message': 'Certificate will be generated soon',
            'certificate_id': str(result.inserted_id)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting course certificate: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Live Class Routes
@student_bp.route('/live-classes', methods=['GET'])
@role_required('student')
def get_live_classes():
    """Get upcoming live classes"""
    current_user = get_current_user()
    course_id = request.args.get('course_id')
    
    liveclass_service = LiveClassService(current_app.db)
    
    if course_id:
        success, classes = liveclass_service.get_course_live_classes(course_id)
    else:
        success, classes = liveclass_service.get_upcoming_classes(current_user['user_id'], 'student')
    
    return jsonify({'success': success, 'live_classes': classes}), 200

@student_bp.route('/live-classes/<class_id>', methods=['GET'])
@role_required('student')
def get_live_class(class_id):
    """Get live class details"""
    liveclass_service = LiveClassService(current_app.db)
    success, live_class = liveclass_service.get_live_class(class_id)
    
    if success:
        return jsonify({'success': True, 'live_class': live_class}), 200
    else:
        return jsonify({'success': False, 'error': 'Live class not found'}), 404

# Payment Routes
@student_bp.route('/payments', methods=['GET'])
@role_required('student')
def get_payments():
    """Get student's payment history"""
    current_user = get_current_user()
    
    payment_service = PaymentService(current_app.db)
    success, payments = payment_service.get_student_payments(current_user['user_id'])
    
    return jsonify({'success': success, 'payments': payments}), 200

@student_bp.route('/payments/create', methods=['POST'])
@role_required('student')
def create_payment():
    """Create payment for course enrollment"""
    current_user = get_current_user()
    data = request.get_json()
    
    payment_service = PaymentService(current_app.db)
    success, message, payment_data = payment_service.create_payment(
        current_user['user_id'],
        data.get('course_id'),
        data.get('amount')
    )
    
    if success:
        return jsonify({'success': True, 'message': message, 'payment': payment_data}), 201
    else:
        return jsonify({'success': False, 'error': message}), 400

@student_bp.route('/payments/<payment_id>/complete', methods=['POST'])
@role_required('student')
def complete_payment(payment_id):
    """Complete payment after gateway response"""
    data = request.get_json()
    
    payment_service = PaymentService(current_app.db)
    success, message = payment_service.process_payment(payment_id, data)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    else:
        return jsonify({'success': False, 'error': message}), 400


@student_bp.route('/courses/<course_id>/materials', methods=['GET'])
@role_required('student')
def get_course_materials(course_id):
    """Get all materials for a course"""
    try:
        db = current_app.db
        materials = list(db.materials.find({'course_id': course_id}))
        
        # Convert ObjectId to string
        for material in materials:
            material['_id'] = str(material['_id'])
        
        return jsonify({
            'success': True,
            'materials': materials
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@student_bp.route('/courses/<course_id>/liveclasses', methods=['GET'])
@role_required('student')
def get_course_liveclasses(course_id):
    """Get all live classes for a course"""
    try:
        liveclass_service = LiveClassService(current_app.db)
        success, live_classes = liveclass_service.get_course_live_classes(course_id)

        if not success:
            return jsonify({'success': False, 'live_classes': []}), 200

        return jsonify({
            'success': True,
            'live_classes': live_classes
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

