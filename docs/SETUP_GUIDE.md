# 🚀 CourseHub - Setup and Run Guide

## ✅ Complete Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python scripts/db_init.py
```

**Expected Output:**
```
🔌 Connecting to MongoDB...
✅ Connected to database: online_course_platform
📊 Creating indexes...
✅ Indexes created successfully

👥 Creating sample users...
✅ Admin created: admin@coursehub.com / Admin@123
✅ Instructor created: sarah@coursehub.com / Instructor@123
✅ Instructor created: michael@coursehub.com / Instructor@123
✅ Student created: john@student.com / Student@123
✅ Student created: jane@student.com / Student@123

📚 Creating sample courses...
✅ Course created: Complete Web Development Bootcamp
✅ Course created: Python Programming Masterclass
✅ Course created: Data Science and Machine Learning
✅ Course created: Introduction to Programming (Free)

✅ Database initialization complete!
```

### Step 3: Run the Application
```bash
python run.py
```

**Expected Output:**
```
🚀 Starting CourseHub Platform...
📍 Access the application at: http://localhost:5000
⚙️  Environment: development
✅ Connected to MongoDB: online_course_platform
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 4: Access the Application
Open your browser and navigate to: **http://localhost:5000**

---

## 👥 Login Credentials

### 🔑 Admin Account
- **URL:** http://localhost:5000/admin/dashboard
- **Email:** admin@coursehub.com
- **Password:** Admin@123
- **Capabilities:**
  - Approve/reject courses
  - Manage all users
  - View platform analytics
  - Process refunds

### 👨‍🏫 Instructor Account
- **URL:** http://localhost:5000/instructor/dashboard
- **Email:** sarah@coursehub.com
- **Password:** Instructor@123
- **Capabilities:**
  - Create and manage courses
  - Upload course materials
  - Track student progress
  - View revenue analytics

### 🎓 Student Account
- **URL:** http://localhost:5000/student/dashboard
- **Email:** john@student.com
- **Password:** Student@123
- **Capabilities:**
  - Browse and enroll in courses
  - Track learning progress
  - AI chatbot assistance
  - Get AI recommendations
  - View certificates

---

## 🧪 Testing the Platform

### 1. Test Student Flow
1. Login as student: john@student.com
2. Browse courses
3. Enroll in a free course ("Introduction to Programming")
4. Enroll in a paid course (demo payment)
5. View dashboard with enrolled courses
6. Try the AI chatbot
7. Get AI recommendations

### 2. Test Instructor Flow
1. Login as instructor: sarah@coursehub.com
2. View your courses
3. Create a new course
4. Add course materials
5. Publish the course
6. View student enrollments
7. Check analytics

### 3. Test Admin Flow
1. Login as admin: admin@coursehub.com
2. View pending courses
3. Approve/reject courses
4. View platform statistics
5. Manage users
6. Check revenue analytics

---

## 🤖 Testing AI Features

### AI Chatbot
**Student Dashboard → Click Chatbot Button (💬)**

Sample queries:
- "What courses do you recommend for web development?"
- "How do I get started with Python?"
- "What are the best study tips for online learning?"

### AI Course Recommendations
**Student Dashboard → Recommendations Tab**

The AI will suggest courses based on:
- Your interests
- Skill level
- Completed courses
- Career goals

---

## 📡 API Testing (Optional)

Use Postman or curl to test API endpoints:

### Register a new user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "Test@123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@student.com",
    "password": "Student@123"
  }'
```

### Get Courses (with JWT token)
```bash
curl -X GET http://localhost:5000/api/student/courses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🗂️ Project Structure Overview

```
course_system/
├── app/                       # Main application
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration
│   ├── models/               # MongoDB models
│   ├── routes/               # API endpoints
│   ├── services/             # Business logic
│   └── utils/                # Utilities
│
├── templates/                # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── student_dashboard.html
│   ├── instructor_dashboard.html
│   └── admin_dashboard.html
│
├── static/
│   └── js/
│       └── api-client.js     # Frontend API client
│
├── scripts/
│   └── db_init.py            # Database initialization
│
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── run.py                    # Application entry point
```

---

## 🔧 Configuration

### Environment Variables (.env)
```
MONGO_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_change_this_in_production
DATABASE_NAME=online_course_platform
```

See `.env.example` for a template.

### MongoDB Collections Created:
- `users` - User accounts
- `courses` - Course catalog
- `enrollments` - Student enrollments
- `progress` - Learning progress tracking
- `payments` - Payment records

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Error
**Solution:** Check your internet connection and MongoDB URI in `.env`

### Issue: Import Errors
**Solution:** Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Issue: Port 5000 Already in Use
**Solution:** Change port in `run.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue: Groq API Errors
**Solution:** Verify your Groq API key in `.env` file

---

## 📊 Key Features Checklist

✅ User Authentication (JWT)  
✅ Role-Based Access Control  
✅ Course Management  
✅ Enrollment System  
✅ Progress Tracking  
✅ Payment Processing (Demo)  
✅ AI Chatbot (Groq LLM)  
✅ AI Recommendations  
✅ Learning Analytics  
✅ Admin Dashboard  
✅ Instructor Dashboard  
✅ Student Dashboard  
✅ RESTful API  
✅ MongoDB Integration  

---

## 🎯 Next Steps

1. ✅ Run database initialization
2. ✅ Start the Flask application
3. ✅ Login with sample credentials
4. ✅ Test all three user roles
5. ✅ Try AI features (chatbot & recommendations)
6. ✅ Create your own courses as instructor
7. ✅ Enroll in courses as student

---

## 📞 Support

If you encounter any issues:
1. Check the logs in `logs/` directory
2. Verify all environment variables are set
3. Ensure MongoDB connection is working
4. Check Python version (3.8+)

---

**Happy Learning! 🎓**
