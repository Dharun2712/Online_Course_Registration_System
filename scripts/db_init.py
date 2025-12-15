"""
Database Initialization Script
Sets up MongoDB indexes and creates sample data
"""
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user_model import User
from app.models.course_model import Course
from app.models.enrollment_model import Enrollment
from app.models.payment_model import Payment
from app.models.progress_model import Progress

def init_database():
    """Initialize database with indexes and sample data"""
    
    # Connect to MongoDB
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'online_course_platform')
    
    print(f"🔌 Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    print(f"✅ Connected to database: {DATABASE_NAME}")
    
    # Initialize models (this creates indexes)
    print("📊 Creating indexes...")
    user_model = User(db)
    course_model = Course(db)
    enrollment_model = Enrollment(db)
    payment_model = Payment(db)
    progress_model = Progress(db)
    print("✅ Indexes created successfully")
    
    # Create sample users
    print("\n👥 Creating sample users...")
    
    # Admin user
    admin_id = user_model.create(
        name="Admin User",
        email="admin@coursehub.com",
        password="Admin@123",
        role="admin"
    )
    if admin_id:
        print(f"✅ Admin created: admin@coursehub.com / Admin@123")
    else:
        print("ℹ️  Admin user already exists")
    
    # Instructor users
    instructor1_id = user_model.create(
        name="Dr. Sarah Johnson",
        email="sarah@coursehub.com",
        password="Instructor@123",
        role="instructor",
        bio="PhD in Computer Science, 10+ years teaching experience"
    )
    if instructor1_id:
        print(f"✅ Instructor created: sarah@coursehub.com / Instructor@123")
    
    instructor2_id = user_model.create(
        name="Prof. Michael Chen",
        email="michael@coursehub.com",
        password="Instructor@123",
        role="instructor",
        bio="Expert in Data Science and Machine Learning"
    )
    if instructor2_id:
        print(f"✅ Instructor created: michael@coursehub.com / Instructor@123")
    
    # Student users
    student1_id = user_model.create(
        name="John Doe",
        email="john@student.com",
        password="Student@123",
        role="student"
    )
    if student1_id:
        print(f"✅ Student created: john@student.com / Student@123")
    
    student2_id = user_model.create(
        name="Jane Smith",
        email="jane@student.com",
        password="Student@123",
        role="student"
    )
    if student2_id:
        print(f"✅ Student created: jane@student.com / Student@123")
    
    # Create sample courses
    print("\n📚 Creating sample courses...")
    
    # Get instructor IDs
    instructor1 = user_model.find_by_email("sarah@coursehub.com")
    instructor2 = user_model.find_by_email("michael@coursehub.com")
    
    if instructor1:
        # Course 1
        course1_id = course_model.create(
            title="Complete Web Development Bootcamp",
            description="Learn HTML, CSS, JavaScript, React, Node.js, and MongoDB. Build 15+ projects and become a full-stack web developer.",
            instructor_id=instructor1['_id'],
            price=49.99,
            tags=["Web Development", "JavaScript", "React", "Node.js"],
            duration="12 weeks",
            level="Beginner"
        )
        if course1_id:
            course_model.approve_course(course1_id)
            course_model.publish_course(course1_id)
            print(f"✅ Course created: Complete Web Development Bootcamp")
        
        # Course 2
        course2_id = course_model.create(
            title="Python Programming Masterclass",
            description="Master Python programming from basics to advanced. Includes OOP, data structures, web scraping, and automation.",
            instructor_id=instructor1['_id'],
            price=39.99,
            tags=["Python", "Programming", "Automation"],
            duration="8 weeks",
            level="Beginner"
        )
        if course2_id:
            course_model.approve_course(course2_id)
            course_model.publish_course(course2_id)
            print(f"✅ Course created: Python Programming Masterclass")
    
    if instructor2:
        # Course 3
        course3_id = course_model.create(
            title="Data Science and Machine Learning with Python",
            description="Learn data analysis, visualization, and machine learning. Work with NumPy, Pandas, Matplotlib, and Scikit-learn.",
            instructor_id=instructor2['_id'],
            price=59.99,
            tags=["Data Science", "Machine Learning", "Python", "AI"],
            duration="10 weeks",
            level="Intermediate"
        )
        if course3_id:
            course_model.approve_course(course3_id)
            course_model.publish_course(course3_id)
            print(f"✅ Course created: Data Science and Machine Learning")
        
        # Course 4 - Free course
        course4_id = course_model.create(
            title="Introduction to Programming",
            description="Beginner-friendly introduction to programming concepts. No prior experience required!",
            instructor_id=instructor2['_id'],
            price=0,
            tags=["Programming", "Beginner", "Fundamentals"],
            duration="4 weeks",
            level="Beginner"
        )
        if course4_id:
            course_model.approve_course(course4_id)
            course_model.publish_course(course4_id)
            print(f"✅ Course created: Introduction to Programming (Free)")
    
    print("\n✅ Database initialization complete!")
    print("\n" + "="*60)
    print("📝 SAMPLE CREDENTIALS")
    print("="*60)
    print("\nAdmin:")
    print("  Email: admin@coursehub.com")
    print("  Password: Admin@123")
    print("\nInstructor:")
    print("  Email: sarah@coursehub.com")
    print("  Password: Instructor@123")
    print("\nStudent:")
    print("  Email: john@student.com")
    print("  Password: Student@123")
    print("="*60)
    
    client.close()

if __name__ == "__main__":
    init_database()
