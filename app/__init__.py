from flask import Flask, render_template
from flask_cors import CORS
from pymongo import MongoClient
import os
from app.config import config

def create_app(config_name='default'):
    """Flask application factory"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # MongoDB connection
    try:
        # Try local MongoDB first for development
        local_uri = 'mongodb://localhost:27017'
        print(f"Attempting local MongoDB connection at {local_uri}...")
        client = MongoClient(local_uri, serverSelectionTimeoutMS=2000)
        client.server_info()
        db = client[app.config['DATABASE_NAME']]
        app.db = db
        print(f"✅ Connected to local MongoDB: {app.config['DATABASE_NAME']}")
    except Exception as e:
        print(f"❌ Local MongoDB Connection Error: {e}")
        # Try Atlas as fallback
        try:
            primary_uri = app.config.get('MONGO_URI')
            print(f"Attempting MongoDB Atlas fallback...")
            client = MongoClient(primary_uri, serverSelectionTimeoutMS=5000)
            client.server_info()
            db = client[app.config['DATABASE_NAME']]
            app.db = db
            print(f"✅ Connected to MongoDB Atlas: {app.config['DATABASE_NAME']}")
        except Exception as e2:
            print(f"❌ MongoDB Atlas fallback failed: {e2}")
            app.db = None
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.instructor_routes import instructor_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.ai_routes import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(instructor_bp, url_prefix='/api/instructor')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    # HTML routes (serving existing HTML files)
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/courses')
    def courses():
        return render_template('courses.html')
    
    @app.route('/course/<course_id>')
    def course_detail(course_id):
        return render_template('course_detail.html', course_id=course_id)
    
    @app.route('/enroll/<course_id>')
    def enroll(course_id):
        return render_template('enroll.html', course_id=course_id)
    
    @app.route('/payment')
    def payment():
        return render_template('payment.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/student/dashboard')
    def student_dashboard():
        return render_template('student_dashboard.html')
    
    @app.route('/instructor/login')
    def instructor_login_page():
        return render_template('instructor_login.html')
    
    @app.route('/instructor/diagnostics')
    def instructor_diagnostics():
        return render_template('dashboard_diagnostics.html')
    
    @app.route('/instructor/dashboard')
    def instructor_dashboard():
        return render_template('instructor_dashboard_new.html')
    
    @app.route('/instructor/dashboard/old')
    def instructor_dashboard_old():
        return render_template('instructor_dashboard.html')
    
    @app.route('/instructor/create-course')
    def create_course_page():
        return render_template('create_course.html')
    
    @app.route('/admin/dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')
    
    @app.route('/admin/users')
    def admin_users():
        return render_template('admin_users.html')
    
    @app.route('/admin/courses')
    def admin_courses():
        return render_template('admin_courses.html')
    
    @app.route('/admin/enrollments')
    def admin_enrollments():
        return render_template('admin_enrollments.html')
    
    @app.route('/admin/payments')
    def admin_payments():
        return render_template('admin_payments.html')
    
    @app.route('/admin/analytics')
    def admin_analytics():
        return render_template('admin_analytics.html')
    
    @app.route('/course/learn')
    def course_learning():
        return render_template('course_learning.html')
    
    @app.route('/student/exam')
    def take_exam():
        return render_template('take_exam.html')
    
    @app.route('/exam/<exam_id>/take')
    def take_exam_with_id(exam_id):
        return render_template('take_exam.html')
    
    @app.route('/certificate/<certificate_id>')
    def view_certificate(certificate_id):
        """View certificate as HTML page"""
        from app.services.certificate_service import CertificateService
        from bson import ObjectId
        
        cert_service = CertificateService(db)
        success, certificate = cert_service.get_certificate(certificate_id)
        
        if not success or not certificate:
            return "Certificate not found", 404
        
        return render_template('certificate.html', certificate=certificate)
    
    @app.route('/test-dashboard')
    def test_dashboard():
        return render_template('test_dashboard.html')
    
    @app.route('/test_instructor_dashboard.html')
    def test_instructor_dashboard_file():
        return render_template('test_instructor_dashboard.html')
    
    @app.route('/test_instructor_login.html')
    def test_instructor_login_file():
        return render_template('test_instructor_login.html')
    
    @app.route('/debug_instructor.html')
    def debug_instructor_file():
        return render_template('debug_instructor.html')
    
    @app.route('/instructor/auto-login')
    def instructor_auto_login():
        return render_template('instructor_auto_login.html')
    
    @app.route('/instructor/quick-fix')
    def instructor_quick_fix():
        return render_template('instructor_quick_fix.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    return app
