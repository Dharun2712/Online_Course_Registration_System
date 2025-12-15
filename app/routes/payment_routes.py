"""
Payment Routes
Handles payment processing (Demo implementation)
"""
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import role_required, get_current_user
from app.models.payment_model import Payment
from app.models.course_model import Course

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/demo', methods=['POST'])
@role_required('student')
def demo_payment():
    """
    Process demo payment (automatically successful)
    In production, integrate with real payment gateway
    """
    current_user = get_current_user()
    data = request.get_json()
    
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'success': False, 'error': 'Course ID required'}), 400
    
    # Get course details
    course_model = Course(current_app.db)
    course = course_model.find_by_id(course_id)
    
    if not course:
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    
    # Create payment record
    payment_model = Payment(current_app.db)
    payment_id = payment_model.create(
        student_id=current_user['user_id'],
        course_id=course_id,
        amount=course['price'],
        payment_method='demo',
        status='completed'
    )
    
    if payment_id:
        payment = payment_model.find_by_id(payment_id)
        return jsonify({
            'success': True,
            'message': 'Payment processed successfully (Demo)',
            'payment': payment
        }), 201
    else:
        return jsonify({'success': False, 'error': 'Payment failed'}), 400

@payment_bp.route('/my-payments', methods=['GET'])
@role_required('student')
def get_my_payments():
    """Get all payments made by student"""
    current_user = get_current_user()
    
    payment_model = Payment(current_app.db)
    payments = payment_model.get_student_payments(current_user['user_id'])
    
    # Enrich with course details
    course_model = Course(current_app.db)
    for payment in payments:
        course = course_model.find_by_id(payment['course_id'])
        payment['course'] = course
    
    return jsonify({
        'success': True,
        'payments': payments
    }), 200

@payment_bp.route('/course/<course_id>/payments', methods=['GET'])
@role_required('instructor')
def get_course_payments(course_id):
    """Get all payments for a specific course (instructor only)"""
    current_user = get_current_user()
    
    # Verify instructor owns this course
    course_model = Course(current_app.db)
    course = course_model.find_by_id(course_id)
    
    if not course or course['instructor_id'] != current_user['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    payment_model = Payment(current_app.db)
    payments = payment_model.get_course_payments(course_id)
    
    return jsonify({
        'success': True,
        'payments': payments
    }), 200

@payment_bp.route('/<payment_id>', methods=['GET'])
@role_required('student')
def get_payment_details(payment_id):
    """Get payment details"""
    current_user = get_current_user()
    
    payment_model = Payment(current_app.db)
    payment = payment_model.find_by_id(payment_id)
    
    if not payment:
        return jsonify({'success': False, 'error': 'Payment not found'}), 404
    
    # Verify user owns this payment
    if payment['student_id'] != current_user['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Enrich with course details
    course_model = Course(current_app.db)
    course = course_model.find_by_id(payment['course_id'])
    payment['course'] = course
    
    return jsonify({
        'success': True,
        'payment': payment
    }), 200

@payment_bp.route('/verify/<course_id>', methods=['GET'])
@role_required('student')
def verify_payment(course_id):
    """Verify if student has paid for a course"""
    current_user = get_current_user()
    
    payment_model = Payment(current_app.db)
    has_paid = payment_model.has_paid_for_course(current_user['user_id'], course_id)
    
    return jsonify({
        'success': True,
        'has_paid': has_paid
    }), 200

@payment_bp.route('/<payment_id>/refund', methods=['POST'])
@role_required('admin')
def process_refund(payment_id):
    """Process refund (admin only)"""
    data = request.get_json()
    refund_amount = data.get('refund_amount')
    
    payment_model = Payment(current_app.db)
    success = payment_model.process_refund(payment_id, refund_amount)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Refund processed successfully'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to process refund'
        }), 400
