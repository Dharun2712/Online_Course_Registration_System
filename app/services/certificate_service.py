"""
Certificate Service
Handles e-certificate generation and email delivery
"""
from datetime import datetime
from bson import ObjectId
import base64
from io import BytesIO
import os

# PDF generation library (reportlab). If not installed, PDF generation will fail gracefully.
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

class CertificateService:
    def __init__(self, db):
        self.db = db
        self.certificate_collection = db['certificates']
        self.submission_collection = db['exam_submissions']
        self.users_collection = db['users']
        self.courses_collection = db['courses']
        
    def generate_certificate(self, submission_id, admin_id):
        """Generate certificate after admin approval"""
        try:
            # Get submission
            submission = self.submission_collection.find_one({'_id': ObjectId(submission_id)})
            if not submission:
                return False, 'Submission not found'
            
            # Check if passed
            if not submission.get('passed'):
                return False, 'Student did not pass the exam'
            
            # Check if already generated
            existing = self.certificate_collection.find_one({
                'submission_id': ObjectId(submission_id)
            })
            
            if existing:
                return False, 'Certificate already generated'
            
            # Get student and course details
            student = self.users_collection.find_one({'_id': submission['student_id']})
            course = self.courses_collection.find_one({'_id': submission['course_id']})
            
            if not student or not course:
                return False, 'Student or course not found'
            
            # Generate certificate ID
            cert_id = f"CERT-{datetime.now().strftime('%Y%m%d')}-{str(submission['student_id'])[-6:]}"
            
            certificate_doc = {
                'certificate_id': cert_id,
                'submission_id': ObjectId(submission_id),
                'student_id': submission['student_id'],
                'course_id': submission['course_id'],
                'student_name': student['name'],
                'student_email': student['email'],
                'course_title': course['title'],
                'marks_obtained': submission['marks_obtained'],
                'total_marks': submission['total_marks'],
                'percentage': round((submission['marks_obtained'] / submission['total_marks']) * 100, 2),
                'issued_date': datetime.now(),
                'admin_id': ObjectId(admin_id),
                'status': 'active',
                'email_sent': False
            }
            
            result = self.certificate_collection.insert_one(certificate_doc)
            
            # Update submission
            self.submission_collection.update_one(
                {'_id': ObjectId(submission_id)},
                {
                    '$set': {
                        'certificate_generated': True,
                        'admin_approved': True,
                        'certificate_id': str(result.inserted_id)
                    }
                }
            )

            # Create PDF certificate file (if reportlab available)
            try:
                certs_dir = os.path.join(os.getcwd(), 'certificates')
                os.makedirs(certs_dir, exist_ok=True)
                pdf_filename = f"{cert_id}.pdf"
                file_path = os.path.join(certs_dir, pdf_filename)

                if REPORTLAB_AVAILABLE:
                    self._create_pdf(certificate_doc, file_path)
                    # Update certificate doc with file path
                    self.certificate_collection.update_one(
                        {'_id': result.inserted_id},
                        {'$set': {'file_path': file_path}}
                    )
                    # Update submission with certificate path as well
                    self.submission_collection.update_one(
                        {'_id': ObjectId(submission_id)},
                        {'$set': {'certificate_path': file_path}}
                    )
                else:
                    # reportlab not available, leave file_path empty and still return certificate id
                    file_path = None

            except Exception as e:
                print(f"[CertificateService] Error creating PDF: {e}")
                file_path = None

            # Send email (placeholder - implement with actual email service)
            self._send_certificate_email(student['email'], certificate_doc)

            return True, str(result.inserted_id)
            
        except Exception as e:
            return False, f'Error generating certificate: {str(e)}'
    
    def _send_certificate_email(self, email, certificate_data):
        """Send certificate via email"""
        try:
            # This is a placeholder - implement with actual email service (SMTP, SendGrid, etc.)
            print(f"Sending certificate to {email}")
            print(f"Certificate ID: {certificate_data['certificate_id']}")
            
            # Update certificate status
            self.certificate_collection.update_one(
                {'certificate_id': certificate_data['certificate_id']},
                {
                    '$set': {
                        'email_sent': True,
                        'email_sent_at': datetime.now()
                    }
                }
            )
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def _create_pdf(self, certificate_data, file_path):
        """Create a professional PDF certificate with template background"""
        if not REPORTLAB_AVAILABLE:
            # Use fallback minimal PDF generator
            return self._create_simple_pdf(file_path, certificate_data)

        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor, black, white
        from reportlab.lib.utils import ImageReader
        from PIL import Image

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4  # 595.27 x 841.89 points

        # Try to use template image as background
        template_path = os.path.join(os.getcwd(), 'static', 'certificate_templates', 'certificate_template.png')
        
        if os.path.exists(template_path):
            # Draw template image as background - fit to A4 size
            try:
                # Get image dimensions to maintain aspect ratio
                img = Image.open(template_path)
                img_width, img_height = img.size
                
                # Calculate scaling to fit A4 while maintaining aspect ratio
                scale_w = width / img_width
                scale_h = height / img_height
                scale = min(scale_w, scale_h)
                
                new_width = img_width * scale
                new_height = img_height * scale
                
                # Center the image on page
                x = (width - new_width) / 2
                y = (height - new_height) / 2
                
                c.drawImage(template_path, x, y, width=new_width, height=new_height, preserveAspectRatio=True, mask='auto')
            except Exception as e:
                print(f"[CertificateService] Error loading template image: {e}")
                # Fall back to solid background
                c.setFillColor(HexColor('#F5F5DC'))
                c.rect(0, 0, width, height, fill=1)
        else:
            print(f"[CertificateService] Template not found at: {template_path}")
            # Solid background if template not found
            c.setFillColor(HexColor('#F5F5DC'))
            c.rect(0, 0, width, height, fill=1)

        # Student Name - positioned to match template (adjust Y position as needed)
        c.setFillColor(black)
        c.setFont('Helvetica-Bold', 32)
        # Center horizontally, position at ~45% from top
        c.drawCentredString(width/2, height * 0.45, certificate_data.get('student_name', '').upper())

        # Award text - positioned below name
        course_title = certificate_data.get('course_title', '')
        issued_date = certificate_data.get('issued_date')
        year = issued_date.year if issued_date else 2025
        
        award_text = f'"Awarded in recognition of outstanding performance in the'
        c.setFont('Helvetica', 13)
        c.drawCentredString(width/2, height * 0.38, award_text)
        
        completion_text = f'completion of the {course_title} course on {year}.'
        c.drawCentredString(width/2, height * 0.35, completion_text)

        # Save PDF
        c.showPage()
        c.save()
        
        return True
        c.setFont('Helvetica', 9)
        cert_id_text = f"Certificate ID: {certificate_data.get('certificate_id')}"
        c.drawCentredString(width/2, 18, cert_id_text)
        
        # Issue date
        if issued_date:
            c.setFillColor(dark_gray)
            c.setFont('Helvetica-Oblique', 8)
            c.drawRightString(width - 50, 18, f"Issued: {issued_date.strftime('%B %d, %Y')}")

        c.showPage()
        c.save()

    def _create_simple_pdf(self, file_path, certificate_data):
        """Fallback minimal PDF writer that writes plain text to a PDF using Type1 fonts.
        This is intentionally minimal and avoids external deps.
        """
        try:
            title = 'Certificate of Completion'
            name = certificate_data.get('student_name', '')
            course = certificate_data.get('course_title', '')
            score = f"Score: {certificate_data.get('marks_obtained')}/{certificate_data.get('total_marks')} ({certificate_data.get('percentage')}%)"
            issued = certificate_data.get('issued_date').strftime('%Y-%m-%d') if certificate_data.get('issued_date') else ''

            text = f"{title}\n\n{name}\n\nhas successfully completed the course:\n{course}\n\n{score}\nIssued: {issued}\nCertificate ID: {certificate_data.get('certificate_id')}"

            # Build very simple PDF with single text block
            content_stream = "BT\n/F1 14 Tf\n50 700 Td\n(%s) Tj\nET\n" % text.replace('(', '\(').replace(')', '\)')
            content_bytes = content_stream.encode('utf-8')

            objs = []
            # Obj 1: Catalog
            objs.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
            # Obj 2: Pages
            objs.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
            # Obj 3: Page
            media = b"[0 0 595 842]"
            objs.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox " + media + b" /Contents 4 0 R >>\nendobj\n")
            # Obj 4: Contents
            objs.append(b"4 0 obj\n<< /Length %d >>\nstream\n" % len(content_bytes) + content_bytes + b"\nendstream\nendobj\n")

            # Build xref
            body = b""
            offsets = []
            for o in objs:
                offsets.append(len(body))
                body += o

            xref_pos = len(body)
            xref = b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
            for off in offsets:
                xref += b"%010d 00000 n \n" % off

            trailer = b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%EOF\n" % (len(objs) + 1, xref_pos)

            pdf_bytes = b"%PDF-1.1\n" + body + xref + trailer

            with open(file_path, 'wb') as f:
                f.write(pdf_bytes)

            return True
        except Exception as e:
            print(f"[CertificateService] simple PDF generation failed: {e}")
            return False

    def render_certificate_pdf(self, certificate_id):
        """Ensure a PDF file exists for a certificate; create on-demand if missing.
        Returns tuple (success, file_path_or_error)
        """
        try:
            cert = self.certificate_collection.find_one({'_id': ObjectId(certificate_id)})
            if not cert:
                return False, 'Certificate not found'

            file_path = cert.get('file_path')
            if file_path and os.path.exists(file_path):
                return True, file_path

            # Otherwise create a file
            certs_dir = os.path.join(os.getcwd(), 'certificates')
            os.makedirs(certs_dir, exist_ok=True)
            pdf_filename = f"{cert.get('certificate_id')}.pdf"
            file_path = os.path.join(certs_dir, pdf_filename)

            # call _create_pdf or fallback
            created = False
            if REPORTLAB_AVAILABLE:
                # _create_pdf returns None when successful (reportlab), so check file existence
                self._create_pdf(cert, file_path)
                created = os.path.exists(file_path)
            else:
                created = self._create_simple_pdf(file_path, cert)

            if created:
                self.certificate_collection.update_one({'_id': cert['_id']}, {'$set': {'file_path': file_path}})
                return True, file_path
            else:
                return False, 'Failed to create certificate PDF'
        except Exception as e:
            print(f"[CertificateService] render_certificate_pdf error: {e}")
            return False, str(e)
    
    def get_student_certificates(self, student_id):
        """Get all certificates for a student"""
        try:
            certificates = list(self.certificate_collection.find({
                'student_id': ObjectId(student_id)
            }).sort('issued_date', -1))
            
            for cert in certificates:
                cert['_id'] = str(cert['_id'])
                cert['submission_id'] = str(cert['submission_id'])
                cert['student_id'] = str(cert['student_id'])
                cert['course_id'] = str(cert['course_id'])
                cert['admin_id'] = str(cert['admin_id'])
                cert['issued_date'] = cert['issued_date'].isoformat()
            
            return True, certificates
            
        except Exception as e:
            return False, []
    
    def get_certificate(self, certificate_id):
        """Get certificate by ID"""
        try:
            if ObjectId.is_valid(certificate_id):
                cert = self.certificate_collection.find_one({'_id': ObjectId(certificate_id)})
            else:
                cert = self.certificate_collection.find_one({'certificate_id': certificate_id})
            
            if not cert:
                return False, None
            
            cert['_id'] = str(cert['_id'])
            cert['submission_id'] = str(cert['submission_id'])
            cert['student_id'] = str(cert['student_id'])
            cert['course_id'] = str(cert['course_id'])
            cert['admin_id'] = str(cert['admin_id'])
            cert['issued_date'] = cert['issued_date'].isoformat()
            
            return True, cert
            
        except Exception as e:
            return False, None
    
    def get_pending_approvals(self):
        """Get submissions pending certificate approval"""
        try:
            # Find passed submissions without certificates
            submissions = list(self.submission_collection.find({
                'passed': True,
                'graded': True,
                'certificate_generated': False
            }))
            
            pending = []
            for sub in submissions:
                student = self.users_collection.find_one({'_id': sub['student_id']})
                course = self.courses_collection.find_one({'_id': sub['course_id']})
                
                pending.append({
                    'submission_id': str(sub['_id']),
                    'student_id': str(sub['student_id']),
                    'student_name': student['name'] if student else 'Unknown',
                    'student_email': student['email'] if student else 'Unknown',
                    'course_id': str(sub['course_id']),
                    'course_title': course['title'] if course else 'Unknown',
                    'marks_obtained': sub['marks_obtained'],
                    'total_marks': sub['total_marks'],
                    'submitted_at': sub['submitted_at'].isoformat()
                })
            
            return True, pending
            
        except Exception as e:
            return False, []
    
    def revoke_certificate(self, certificate_id, admin_id, reason):
        """Revoke a certificate"""
        try:
            result = self.certificate_collection.update_one(
                {'_id': ObjectId(certificate_id)},
                {
                    '$set': {
                        'status': 'revoked',
                        'revoked_by': ObjectId(admin_id),
                        'revoked_at': datetime.now(),
                        'revocation_reason': reason
                    }
                }
            )
            
            if result.modified_count > 0:
                return True, 'Certificate revoked successfully'
            else:
                return False, 'Certificate not found'
            
        except Exception as e:
            return False, f'Error revoking certificate: {str(e)}'
