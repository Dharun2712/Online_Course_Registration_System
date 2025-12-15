"""
Payment Model - Handles course payments (Demo implementation)
"""
from datetime import datetime
from bson import ObjectId
import random
import string

class Payment:
    def __init__(self, db):
        self.collection = db['payments']
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for better performance"""
        self.collection.create_index("student_id")
        self.collection.create_index("course_id")
        self.collection.create_index("transaction_id", unique=True)
        self.collection.create_index("status")
    
    def _generate_transaction_id(self):
        """Generate unique transaction ID"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TXN{timestamp}{random_str}"
    
    def create(self, student_id, course_id, amount, payment_method="demo", status="completed"):
        """
        Create a payment record (Demo - automatically successful)
        Args:
            student_id: Student making the payment
            course_id: Course being purchased
            amount: Payment amount
            payment_method: Payment method (demo/card/paypal/etc)
            status: Payment status (completed/pending/failed)
        Returns:
            ObjectId of payment record
        """
        payment_data = {
            "transaction_id": self._generate_transaction_id(),
            "student_id": str(student_id),
            "course_id": str(course_id),
            "amount": float(amount),
            "currency": "USD",
            "payment_method": payment_method,
            "status": status,  # completed/pending/failed/refunded
            "metadata": {
                "ip_address": "127.0.0.1",
                "user_agent": "Demo Payment"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(payment_data)
        return result.inserted_id
    
    def find_by_id(self, payment_id):
        """Find payment by ID"""
        try:
            payment = self.collection.find_one({"_id": ObjectId(payment_id)})
            if payment:
                payment['_id'] = str(payment['_id'])
            return payment
        except:
            return None
    
    def find_by_transaction_id(self, transaction_id):
        """Find payment by transaction ID"""
        payment = self.collection.find_one({"transaction_id": transaction_id})
        if payment:
            payment['_id'] = str(payment['_id'])
        return payment
    
    def get_student_payments(self, student_id):
        """Get all payments made by a student"""
        payments = list(self.collection.find(
            {"student_id": str(student_id)}
        ).sort("created_at", -1))
        
        for payment in payments:
            payment['_id'] = str(payment['_id'])
        return payments
    
    def get_course_payments(self, course_id):
        """Get all payments for a specific course"""
        payments = list(self.collection.find(
            {"course_id": str(course_id)}
        ).sort("created_at", -1))
        
        for payment in payments:
            payment['_id'] = str(payment['_id'])
        return payments
    
    def has_paid_for_course(self, student_id, course_id):
        """Check if student has successfully paid for a course"""
        payment = self.collection.find_one({
            "student_id": str(student_id),
            "course_id": str(course_id),
            "status": "completed"
        })
        return payment is not None
    
    def update_status(self, payment_id, status):
        """Update payment status"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": {
                    "status": status,
                    "updated_at": datetime.utcnow()
                }}
            )
            return result.modified_count > 0
        except:
            return False
    
    def process_refund(self, payment_id, refund_amount=None):
        """
        Process refund for a payment
        Args:
            payment_id: Payment ID to refund
            refund_amount: Amount to refund (None = full refund)
        """
        try:
            payment = self.find_by_id(payment_id)
            if not payment or payment['status'] != 'completed':
                return False
            
            amount = refund_amount if refund_amount else payment['amount']
            
            result = self.collection.update_one(
                {"_id": ObjectId(payment_id)},
                {"$set": {
                    "status": "refunded",
                    "refund_amount": float(amount),
                    "refunded_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }}
            )
            return result.modified_count > 0
        except:
            return False
    
    def get_revenue_statistics(self, instructor_id=None, start_date=None, end_date=None):
        """
        Get revenue statistics
        Args:
            instructor_id: Filter by instructor (optional)
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)
        """
        # Build query
        query = {"status": "completed"}
        
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["created_at"] = date_query
        
        # If instructor_id provided, need to join with courses
        # For simplicity, we'll do basic stats without instructor filter
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "total_revenue": {"$sum": "$amount"},
                "total_transactions": {"$sum": 1},
                "avg_transaction": {"$avg": "$amount"}
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        
        if result:
            stats = result[0]
            return {
                "total_revenue": round(stats.get("total_revenue", 0), 2),
                "total_transactions": stats.get("total_transactions", 0),
                "average_transaction": round(stats.get("avg_transaction", 0), 2)
            }
        
        return {
            "total_revenue": 0,
            "total_transactions": 0,
            "average_transaction": 0
        }
    
    def get_monthly_revenue(self, year):
        """Get monthly revenue breakdown for a year"""
        pipeline = [
            {
                "$match": {
                    "status": "completed",
                    "created_at": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1)
                    }
                }
            },
            {
                "$group": {
                    "_id": {"$month": "$created_at"},
                    "revenue": {"$sum": "$amount"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        monthly_data = {i: {"revenue": 0, "count": 0} for i in range(1, 13)}
        for result in results:
            month = result['_id']
            monthly_data[month] = {
                "revenue": round(result['revenue'], 2),
                "count": result['count']
            }
        
        return monthly_data
