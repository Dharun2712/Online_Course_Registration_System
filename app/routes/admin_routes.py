"""
Admin Routes
Handles admin-specific operations
"""
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import role_required, get_current_user
from app.models.user_model import User
from app.models.course_model import Course
from app.models.enrollment_model import Enrollment
from app.models.payment_model import Payment
from app.services.certificate_service import CertificateService
from app.services.payment_service import PaymentService
from app.services.analytics_service import AnalyticsService
from app.services.exam_service import ExamService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_all_users():
    """Get all users"""
    role = request.args.get('role')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    user_model = User(current_app.db)
    skip = (page - 1) * per_page
    
    users = user_model.get_all_users(role, skip, per_page)
    
    return jsonify({
        'success': True,
        'users': users,
        'page': page,
        'per_page': per_page
    }), 200

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(user_id):
    """Deactivate a user"""
    user_model = User(current_app.db)
    success = user_model.delete(user_id)
    
    if success:
        return jsonify({'success': True, 'message': 'User deactivated'}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to deactivate user'}), 400

@admin_bp.route('/courses/pending', methods=['GET'])
@role_required('admin')
def get_pending_courses():
    """Get all courses pending approval"""
    course_model = Course(current_app.db)
    courses = course_model.get_all_courses({'status': 'pending'})
    
    return jsonify({
        'success': True,
        'courses': courses
    }), 200

@admin_bp.route('/courses', methods=['GET'])
@role_required('admin')
def get_all_courses():
    """Get all courses for admin view"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    course_model = Course(current_app.db)
    skip = (page - 1) * per_page
    
    # Get all courses with instructor info
    courses = list(current_app.db.courses.find().skip(skip).limit(per_page))
    total = current_app.db.courses.count_documents({})
    
    # Enrich with instructor names and enrolled_count
    for course in courses:
        course['_id'] = str(course['_id'])
        instructor = current_app.db.users.find_one({'_id': course.get('instructor_id')})
        course['instructor_name'] = instructor['name'] if instructor else 'Unknown'
        course['instructor_id'] = str(course.get('instructor_id', ''))
        if 'created_at' in course and hasattr(course['created_at'], 'isoformat'):
            course['created_at'] = course['created_at'].isoformat()
        
        # Add enrolled count
        course['enrolled_count'] = current_app.db.enrollments.count_documents({
            'course_id': course['_id'],
            'status': 'active'
        })
    
    return jsonify({
        'success': True,
        'courses': courses,
        'total': total,
        'page': page,
        'per_page': per_page
    }), 200

@admin_bp.route('/courses/<course_id>/approve', methods=['POST'])
@role_required('admin')
def approve_course(course_id):
    """Approve a course"""
    course_model = Course(current_app.db)
    success = course_model.approve_course(course_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Course approved'}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to approve course'}), 400

@admin_bp.route('/courses/<course_id>/reject', methods=['POST'])
@role_required('admin')
def reject_course(course_id):
    """Reject a course"""
    data = request.get_json()
    reason = data.get('reason', 'Does not meet quality standards')
    
    course_model = Course(current_app.db)
    success = course_model.reject_course(course_id, reason)
    
    if success:
        return jsonify({'success': True, 'message': 'Course rejected'}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to reject course'}), 400

@admin_bp.route('/courses/<course_id>', methods=['DELETE'])
@role_required('admin')
def delete_course(course_id):
    """Delete a course"""
    course_model = Course(current_app.db)
    success = course_model.delete(course_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Course deleted'}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to delete course'}), 400

@admin_bp.route('/statistics', methods=['GET'])
@role_required('admin')
def get_platform_statistics():
    """Get platform-wide statistics"""
    user_model = User(current_app.db)
    course_model = Course(current_app.db)
    enrollment_model = Enrollment(current_app.db)
    payment_model = Payment(current_app.db)
    
    # User statistics
    total_users = len(user_model.get_all_users())
    total_students = len(user_model.get_all_users(role='student'))
    total_instructors = len(user_model.get_all_users(role='instructor'))
    
    # Course statistics
    course_stats = course_model.get_statistics()
    
    # Enrollment statistics
    enrollment_stats = enrollment_model.get_statistics()
    
    # Revenue statistics
    revenue_stats = payment_model.get_revenue_statistics()
    
    return jsonify({
        'success': True,
        'statistics': {
            'users': {
                'total': total_users,
                'students': total_students,
                'instructors': total_instructors
            },
            'courses': course_stats,
            'enrollments': enrollment_stats,
            'revenue': revenue_stats
        }
    }), 200

@admin_bp.route('/analytics/monthly-revenue/<int:year>', methods=['GET'])
@role_required('admin')
def get_monthly_revenue(year):
    """Get monthly revenue breakdown"""
    payment_model = Payment(current_app.db)
    monthly_data = payment_model.get_monthly_revenue(year)
    
    return jsonify({
        'success': True,
        'year': year,
        'monthly_revenue': monthly_data
    }), 200

@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin')
def get_dashboard_data():
    """Get comprehensive admin dashboard data"""
    analytics_service = AnalyticsService(current_app.db)
    certificate_service = CertificateService(current_app.db)
    
    # Get comprehensive analytics
    success, analytics = analytics_service.get_admin_analytics()
    
    # Get pending certificate approvals
    _, pending_certificates = certificate_service.get_pending_approvals()
    
    return jsonify({
        'success': True,
        'analytics': analytics if success else {},
        'pending_certificates': pending_certificates
    }), 200

# Certificate Management Routes
@admin_bp.route('/certificates/pending', methods=['GET'])
@role_required('admin')
def get_pending_certificates():
    """Get all submissions pending certificate approval"""
    certificate_service = CertificateService(current_app.db)
    success, pending = certificate_service.get_pending_approvals()
    
    return jsonify({'success': success, 'pending': pending}), 200

@admin_bp.route('/certificates/generate', methods=['POST'])
@role_required('admin')
def generate_certificate():
    """Generate and send certificate for a passed submission"""
    current_user = get_current_user()
    data = request.get_json()
    
    certificate_service = CertificateService(current_app.db)
    success, result = certificate_service.generate_certificate(
        data.get('submission_id'),
        current_user['user_id']
    )
    
    if success:
        return jsonify({'success': True, 'certificate_id': result}), 201
    else:
        return jsonify({'success': False, 'error': result}), 400

@admin_bp.route('/certificates/<certificate_id>/revoke', methods=['POST'])
@role_required('admin')
def revoke_certificate(certificate_id):
    """Revoke a certificate"""
    current_user = get_current_user()
    data = request.get_json()
    
    certificate_service = CertificateService(current_app.db)
    success, message = certificate_service.revoke_certificate(
        certificate_id,
        current_user['user_id'],
        data.get('reason', 'Administrative revocation')
    )
    
    return jsonify({'success': success, 'message': message}), 200 if success else 400

# Payment Management Routes
@admin_bp.route('/payments', methods=['GET'])
@role_required('admin')
def get_all_payments():
    """Get all payment transactions"""
    status = request.args.get('status')
    
    payment_service = PaymentService(current_app.db)
    success, payments = payment_service.get_all_payments(status)
    
    return jsonify({'success': success, 'payments': payments}), 200

@admin_bp.route('/payments/statistics', methods=['GET'])
@role_required('admin')
def get_payment_statistics():
    """Get payment and revenue statistics"""
    payment_service = PaymentService(current_app.db)
    success, stats = payment_service.get_payment_statistics()
    
    return jsonify({'success': success, 'statistics': stats}), 200

@admin_bp.route('/payments/<payment_id>/refund', methods=['POST'])
@role_required('admin')
def refund_payment(payment_id):
    """Process a refund"""
    current_user = get_current_user()
    data = request.get_json()
    
    payment_service = PaymentService(current_app.db)
    success, message = payment_service.refund_payment(
        payment_id,
        current_user['user_id'],
        data.get('reason', 'Administrative refund')
    )
    
    return jsonify({'success': success, 'message': message}), 200 if success else 400

# Student Analytics Routes
@admin_bp.route('/students/<student_id>/analytics', methods=['GET'])
@role_required('admin')
def get_student_complete_analytics(student_id):
    """Get complete analytics for a student"""
    analytics_service = AnalyticsService(current_app.db)
    success, analytics = analytics_service.get_student_analytics(student_id)
    
    # Get payment history
    payment_service = PaymentService(current_app.db)
    _, payments = payment_service.get_student_payments(student_id)
    
    # Get certificates
    certificate_service = CertificateService(current_app.db)
    _, certificates = certificate_service.get_student_certificates(student_id)
    
    # Get exam submissions
    exam_service = ExamService(current_app.db)
    _, submissions = exam_service.get_student_submissions(student_id)
    
    return jsonify({
        'success': True,
        'analytics': analytics if success else {},
        'payments': payments,
        'certificates': certificates,
        'exam_submissions': submissions
    }), 200

@admin_bp.route('/courses/<course_id>/analytics', methods=['GET'])
@role_required('admin')
def get_course_analytics(course_id):
    """Get comprehensive analytics for a course"""
    analytics_service = AnalyticsService(current_app.db)
    success, performance = analytics_service.get_course_performance(course_id)
    
    return jsonify({'success': success, 'analytics': performance}), 200

# User Management - Create Instructor/Admin
@admin_bp.route('/users/create', methods=['POST'])
@role_required('admin')
def create_user():
    """Create instructor or admin account"""
    data = request.get_json()
    role = data.get('role')
    
    if role not in ['instructor', 'admin']:
        return jsonify({'success': False, 'error': 'Can only create instructor or admin accounts'}), 400
    
    from app.services.auth_service import AuthService
    auth_service = AuthService(current_app.db)
    
    success, message, token = auth_service.register(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        role=role
    )
    
    if success:
        return jsonify({
            'success': True,
            'message': f'{role.capitalize()} account created successfully'
        }), 201
    else:
        return jsonify({'success': False, 'error': message}), 400

# Enrollment Management Routes
@admin_bp.route('/enrollments', methods=['GET'])
@role_required('admin')
def get_all_enrollments():
    """Get all enrollments with filters"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    course_id = request.args.get('course_id')
    student_id = request.args.get('student_id')
    status = request.args.get('status')
    
    skip = (page - 1) * per_page
    query = {}
    
    if course_id:
        query['course_id'] = course_id
    if student_id:
        query['student_id'] = student_id
    if status:
        query['status'] = status
    
    enrollments = list(current_app.db.enrollments.find(query).skip(skip).limit(per_page))
    total = current_app.db.enrollments.count_documents(query)
    
    # Enrich with student and course names
    for enrollment in enrollments:
        enrollment['_id'] = str(enrollment['_id'])
        student = current_app.db.users.find_one({'_id': enrollment.get('student_id')})
        course = current_app.db.courses.find_one({'_id': enrollment.get('course_id')})
        
        enrollment['student_name'] = student['name'] if student else 'Unknown'
        enrollment['course_title'] = course['title'] if course else 'Unknown'
        enrollment['student_id'] = str(enrollment.get('student_id', ''))
        enrollment['course_id'] = str(enrollment.get('course_id', ''))
        
        if 'enrolled_at' in enrollment and hasattr(enrollment['enrolled_at'], 'isoformat'):
            enrollment['enrolled_at'] = enrollment['enrolled_at'].isoformat()
    
    return jsonify({
        'success': True,
        'enrollments': enrollments,
        'total': total,
        'page': page,
        'per_page': per_page
    }), 200

@admin_bp.route('/stats', methods=['GET'])
@role_required('admin')
def get_admin_stats():
    """Get real-time admin dashboard statistics"""
    from bson import ObjectId
    from datetime import datetime, timedelta
    
    # Total users count
    total_users = current_app.db.users.count_documents({})
    
    # Total courses count
    total_courses = current_app.db.courses.count_documents({})
    
    # Total revenue (sum all successful payments)
    revenue_pipeline = [
        {'$match': {'status': 'completed'}},
        {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
    ]
    revenue_result = list(current_app.db.payments.aggregate(revenue_pipeline))
    total_revenue = revenue_result[0]['total'] if revenue_result else 0
    
    # Total enrollments
    total_enrollments = current_app.db.enrollments.count_documents({})
    
    # Pending course approvals
    pending_approvals = current_app.db.courses.count_documents({'status': 'pending'})
    
    # Last month comparison for growth percentages
    last_month_start = datetime.now() - timedelta(days=30)
    
    users_last_month = current_app.db.users.count_documents({'created_at': {'$gte': last_month_start}})
    courses_last_month = current_app.db.courses.count_documents({'created_at': {'$gte': last_month_start}})
    enrollments_last_month = current_app.db.enrollments.count_documents({'enrolled_at': {'$gte': last_month_start}})
    
    revenue_last_month_pipeline = [
        {'$match': {'status': 'completed', 'created_at': {'$gte': last_month_start}}},
        {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
    ]
    revenue_last_month_result = list(current_app.db.payments.aggregate(revenue_last_month_pipeline))
    revenue_last_month = revenue_last_month_result[0]['total'] if revenue_last_month_result else 0
    
    # Calculate growth percentages
    def calc_growth(current, last_month):
        if current == 0:
            return 0
        if last_month == 0:
            return 100 if current > 0 else 0
        return round((last_month / current) * 100, 1)
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'users_growth': calc_growth(total_users, users_last_month),
            'total_courses': total_courses,
            'courses_growth': calc_growth(total_courses, courses_last_month),
            'total_revenue': total_revenue,
            'revenue_growth': calc_growth(total_revenue, revenue_last_month),
            'total_enrollments': total_enrollments,
            'enrollments_growth': calc_growth(total_enrollments, enrollments_last_month),
            'pending_approvals': pending_approvals
        }
    }), 200

@admin_bp.route('/analytics/video-completion', methods=['GET'])
@role_required('admin')
def get_video_completion_analytics():
    """Get video completion analytics across all courses"""
    from bson import ObjectId
    
    try:
        # Total videos completed
        total_videos_completed = current_app.db.video_progress.count_documents({'completed': True})
        
        # Total unique students who completed videos
        unique_students = len(current_app.db.video_progress.distinct('student_id'))
        
        # Average completion rate per course
        course_completion_pipeline = [
            {'$match': {'completed': True}},
            {'$group': {
                '_id': '$course_id',
                'completed_count': {'$sum': 1},
                'unique_students': {'$addToSet': '$student_id'}
            }},
            {'$project': {
                'course_id': '$_id',
                'completed_count': 1,
                'student_count': {'$size': '$unique_students'}
            }}
        ]
        
        course_completions = list(current_app.db.video_progress.aggregate(course_completion_pipeline))
        
        # Enrich with course names
        for completion in course_completions:
            try:
                course = current_app.db.courses.find_one({'_id': ObjectId(completion['_id'])})
                completion['course_name'] = course['title'] if course else 'Unknown Course'
                completion['course_id'] = str(completion['_id'])
            except:
                completion['course_name'] = 'Unknown Course'
                completion['course_id'] = str(completion['_id'])
        
        # Recent video completions
        recent_completions = list(current_app.db.video_progress.find(
            {'completed': True}
        ).sort('completed_at', -1).limit(10))
        
        # Enrich recent completions with student and course info
        for completion in recent_completions:
            completion['_id'] = str(completion['_id'])
            completion['student_id'] = str(completion['student_id'])
            completion['course_id'] = str(completion['course_id'])
            
            # Get student name
            try:
                student = current_app.db.users.find_one({'_id': ObjectId(completion['student_id'])})
                completion['student_name'] = student['name'] if student else 'Unknown Student'
            except:
                completion['student_name'] = 'Unknown Student'
            
            # Get course name
            try:
                course = current_app.db.courses.find_one({'_id': ObjectId(completion['course_id'])})
                completion['course_name'] = course['title'] if course else 'Unknown Course'
            except:
                completion['course_name'] = 'Unknown Course'
        
        # Calculate average completion rate
        total_enrollments = current_app.db.enrollments.count_documents({'status': 'active'})
        avg_completion_rate = round((unique_students / total_enrollments * 100), 2) if total_enrollments > 0 else 0
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_videos_completed': total_videos_completed,
                'unique_students': unique_students,
                'avg_completion_rate': avg_completion_rate,
                'course_completions': course_completions,
                'recent_completions': recent_completions
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch video analytics: {str(e)}'
        }), 400
