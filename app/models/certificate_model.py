"""
Certificate Model - E-Certificate Generation and Management
Generates PDF certificates for students who pass exams (score >= 5)
Requires admin approval before email delivery
"""
from datetime import datetime
from bson import ObjectId

class Certificate:
    def __init__(self, db):
        self.collection = db['certificates']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for faster queries"""
        self.collection.create_index([('student_id', 1)])
        self.collection.create_index([('course_id', 1)])
        self.collection.create_index([('exam_id', 1)])
        self.collection.create_index([('admin_approved', 1)])
        self.collection.create_index([('email_sent', 1)])
        # Unique certificate per student per exam
        self.collection.create_index([('student_id', 1), ('exam_id', 1)], unique=True)
    
    def create_certificate(self, cert_data):
        """
        Create a new certificate
        cert_data = {
            'student_id': ObjectId,
            'student_name': str,
            'student_email': str,
            'course_id': ObjectId,
            'course_title': str,
            'exam_id': ObjectId,
            'exam_title': str,
            'score': int,
            'total_marks': int,
            'instructor_name': str,
            'admin_approved': bool (default False),
            'email_sent': bool (default False),
            'certificate_url': str (S3/cloud storage URL)
        }
        """
        certificate = {
            'student_id': cert_data['student_id'],
            'student_name': cert_data['student_name'],
            'student_email': cert_data['student_email'],
            'course_id': cert_data['course_id'],
            'course_title': cert_data['course_title'],
            'exam_id': cert_data['exam_id'],
            'exam_title': cert_data['exam_title'],
            'score': cert_data['score'],
            'total_marks': cert_data['total_marks'],
            'percentage': round((cert_data['score'] / cert_data['total_marks']) * 100, 2),
            'instructor_name': cert_data.get('instructor_name', ''),
            'admin_approved': cert_data.get('admin_approved', False),
            'email_sent': cert_data.get('email_sent', False),
            'certificate_url': cert_data.get('certificate_url', ''),
            'certificate_number': self._generate_certificate_number(),
            'issued_at': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(certificate)
        certificate['_id'] = result.inserted_id
        return self._serialize(certificate)
    
    def get_certificate(self, cert_id):
        """Get certificate by ID"""
        cert = self.collection.find_one({'_id': ObjectId(cert_id)})
        return self._serialize(cert) if cert else None
    
    def get_student_certificates(self, student_id):
        """Get all certificates for a student"""
        certs = list(self.collection.find({'student_id': ObjectId(student_id)}))
        return [self._serialize(cert) for cert in certs]
    
    def get_course_certificates(self, course_id):
        """Get all certificates for a course"""
        certs = list(self.collection.find({'course_id': ObjectId(course_id)}))
        return [self._serialize(cert) for cert in certs]
    
    def get_pending_approvals(self):
        """Get all certificates pending admin approval"""
        certs = list(self.collection.find({'admin_approved': False}))
        return [self._serialize(cert) for cert in certs]
    
    def approve_certificate(self, cert_id, admin_id):
        """Admin approves certificate"""
        self.collection.update_one(
            {'_id': ObjectId(cert_id)},
            {
                '$set': {
                    'admin_approved': True,
                    'approved_by': admin_id,
                    'approved_at': datetime.utcnow()
                }
            }
        )
        return self.get_certificate(cert_id)
    
    def mark_email_sent(self, cert_id):
        """Mark certificate email as sent"""
        self.collection.update_one(
            {'_id': ObjectId(cert_id)},
            {
                '$set': {
                    'email_sent': True,
                    'email_sent_at': datetime.utcnow()
                }
            }
        )
        return self.get_certificate(cert_id)
    
    def update_certificate_url(self, cert_id, url):
        """Update certificate PDF URL"""
        self.collection.update_one(
            {'_id': ObjectId(cert_id)},
            {'$set': {'certificate_url': url}}
        )
        return self.get_certificate(cert_id)
    
    def _generate_certificate_number(self):
        """Generate unique certificate number"""
        # Format: CERT-YYYYMMDD-XXXX
        date_str = datetime.utcnow().strftime('%Y%m%d')
        count = self.collection.count_documents({}) + 1
        return f"CERT-{date_str}-{count:04d}"
    
    def _serialize(self, cert):
        """Convert ObjectId to string"""
        if cert:
            cert['_id'] = str(cert['_id'])
            cert['student_id'] = str(cert['student_id'])
            cert['course_id'] = str(cert['course_id'])
            cert['exam_id'] = str(cert['exam_id'])
            if 'approved_by' in cert:
                cert['approved_by'] = str(cert['approved_by'])
        return cert
