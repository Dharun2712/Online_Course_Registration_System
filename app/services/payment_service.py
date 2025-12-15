"""
Payment Service  
Handles payment processing and transaction tracking
"""
from datetime import datetime
from bson import ObjectId
import secrets

class PaymentService:
    def __init__(self, db):
        self.db = db
        self.payment_collection = db['payments']
        self.enrollment_collection = db['enrollments']
        self.course_collection = db['courses']
        self.users_collection = db['users']
        
    def create_payment(self, student_id, course_id, amount):
        """Create a payment record for course enrollment"""
        try:
            # Get course details
            course = self.course_collection.find_one({'_id': ObjectId(course_id)})
            if not course:
                return False, 'Course not found', None
            
            # Get student details
            student = self.users_collection.find_one({'_id': ObjectId(student_id)})
            if not student:
                return False, 'Student not found', None
            
            # Generate transaction ID
            transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4).upper()}"
            
            payment_doc = {
                'transaction_id': transaction_id,
                'student_id': ObjectId(student_id),
                'course_id': ObjectId(course_id),
                'student_name': student['name'],
                'student_email': student['email'],
                'course_title': course['title'],
                'amount': float(amount),
                'currency': 'USD',
                'payment_method': 'pending',  # Will be updated after payment gateway
                'status': 'pending',
                'created_at': datetime.now(),
                'payment_gateway': 'stripe'  # Placeholder - can be stripe, razorpay, paypal, etc.
            }
            
            result = self.payment_collection.insert_one(payment_doc)
            
            return True, 'Payment record created', {
                'payment_id': str(result.inserted_id),
                'transaction_id': transaction_id,
                'amount': amount
            }
            
        except Exception as e:
            return False, f'Error creating payment: {str(e)}', None
    
    def process_payment(self, payment_id, payment_data):
        """Process payment after gateway response"""
        try:
            payment = self.payment_collection.find_one({'_id': ObjectId(payment_id)})
            if not payment:
                return False, 'Payment record not found'
            
            # Update payment status
            update_data = {
                'status': 'completed',
                'payment_method': payment_data.get('payment_method', 'card'),
                'paid_at': datetime.now(),
                'gateway_transaction_id': payment_data.get('gateway_transaction_id'),
                'gateway_response': payment_data.get('gateway_response', {})
            }
            
            self.payment_collection.update_one(
                {'_id': ObjectId(payment_id)},
                {'$set': update_data}
            )
            
            # Create enrollment (convert IDs to strings for consistency)
            enrollment_doc = {
                'student_id': str(payment['student_id']),
                'course_id': str(payment['course_id']),
                'payment_id': str(payment_id),
                'enrolled_at': datetime.now(),
                'status': 'active',
                'progress': 0,
                'completed': False,
                'completed_materials': [],
                'certificate_issued': False,
                'last_accessed': datetime.now()
            }
            
            self.enrollment_collection.insert_one(enrollment_doc)
            
            return True, 'Payment processed and enrollment created'
            
        except Exception as e:
            return False, f'Error processing payment: {str(e)}'
    
    def get_payment(self, payment_id):
        """Get payment details"""
        try:
            if ObjectId.is_valid(payment_id):
                payment = self.payment_collection.find_one({'_id': ObjectId(payment_id)})
            else:
                payment = self.payment_collection.find_one({'transaction_id': payment_id})
            
            if not payment:
                return False, None
            
            payment['_id'] = str(payment['_id'])
            payment['student_id'] = str(payment['student_id'])
            payment['course_id'] = str(payment['course_id'])
            payment['created_at'] = payment['created_at'].isoformat()
            if 'paid_at' in payment:
                payment['paid_at'] = payment['paid_at'].isoformat()
            
            return True, payment
            
        except Exception as e:
            return False, None
    
    def get_student_payments(self, student_id):
        """Get all payments for a student"""
        try:
            payments = list(self.payment_collection.find({
                'student_id': ObjectId(student_id)
            }).sort('created_at', -1))
            
            for payment in payments:
                payment['_id'] = str(payment['_id'])
                payment['student_id'] = str(payment['student_id'])
                payment['course_id'] = str(payment['course_id'])
                payment['created_at'] = payment['created_at'].isoformat()
                if 'paid_at' in payment:
                    payment['paid_at'] = payment['paid_at'].isoformat()
            
            return True, payments
            
        except Exception as e:
            return False, []
    
    def get_all_payments(self, status=None):
        """Get all payments (admin view)"""
        try:
            query = {}
            if status:
                query['status'] = status
            
            payments = list(self.payment_collection.find(query).sort('created_at', -1))
            
            for payment in payments:
                payment['_id'] = str(payment['_id'])
                payment['student_id'] = str(payment['student_id'])
                payment['course_id'] = str(payment['course_id'])
                payment['created_at'] = payment['created_at'].isoformat()
                if 'paid_at' in payment:
                    payment['paid_at'] = payment['paid_at'].isoformat()
            
            return True, payments
            
        except Exception as e:
            return False, []
    
    def get_payment_statistics(self):
        """Get payment statistics for admin dashboard"""
        try:
            # Total revenue
            pipeline_revenue = [
                {'$match': {'status': 'completed'}},
                {'$group': {
                    '_id': None,
                    'total_revenue': {'$sum': '$amount'},
                    'total_transactions': {'$sum': 1}
                }}
            ]
            
            revenue_result = list(self.payment_collection.aggregate(pipeline_revenue))
            total_revenue = revenue_result[0]['total_revenue'] if revenue_result else 0
            total_transactions = revenue_result[0]['total_transactions'] if revenue_result else 0
            
            # Pending payments
            pending_count = self.payment_collection.count_documents({'status': 'pending'})
            
            # Revenue by course
            pipeline_course = [
                {'$match': {'status': 'completed'}},
                {'$group': {
                    '_id': '$course_id',
                    'revenue': {'$sum': '$amount'},
                    'enrollments': {'$sum': 1}
                }},
                {'$sort': {'revenue': -1}},
                {'$limit': 10}
            ]
            
            course_revenue = list(self.payment_collection.aggregate(pipeline_course))
            
            # Get course titles
            for item in course_revenue:
                course = self.course_collection.find_one({'_id': item['_id']})
                item['course_id'] = str(item['_id'])
                item['course_title'] = course['title'] if course else 'Unknown'
                del item['_id']
            
            return True, {
                'total_revenue': round(total_revenue, 2),
                'total_transactions': total_transactions,
                'pending_payments': pending_count,
                'top_courses_by_revenue': course_revenue
            }
            
        except Exception as e:
            return False, {}
    
    def refund_payment(self, payment_id, admin_id, reason):
        """Process refund for a payment"""
        try:
            payment = self.payment_collection.find_one({'_id': ObjectId(payment_id)})
            if not payment:
                return False, 'Payment not found'
            
            if payment['status'] != 'completed':
                return False, 'Can only refund completed payments'
            
            # Update payment status
            self.payment_collection.update_one(
                {'_id': ObjectId(payment_id)},
                {
                    '$set': {
                        'status': 'refunded',
                        'refunded_at': datetime.now(),
                        'refunded_by': ObjectId(admin_id),
                        'refund_reason': reason
                    }
                }
            )
            
            # Deactivate enrollment
            self.enrollment_collection.update_one(
                {'payment_id': ObjectId(payment_id)},
                {'$set': {'status': 'cancelled'}}
            )
            
            return True, 'Payment refunded successfully'
            
        except Exception as e:
            return False, f'Error processing refund: {str(e)}'
