# 📚 CourseHub - Online Course Registration Platform

A fully-featured online course platform built with **Flask**, **MongoDB**, and **Groq AI (Llama 3.3-70B)**.

## ✨ Features

### 🎓 For Students
- Browse and search courses
- Enroll in courses (free and paid)
- Track learning progress
- AI-powered course recommendations
- AI chatbot for course assistance
- Learning analytics dashboard
- Certificates upon completion

### 👨‍🏫 For Instructors
- Create and manage courses
- Upload course materials
- Track student progress
- View analytics and revenue
- Course approval workflow

### 👑 For Admins
- Approve/reject courses
- Manage users and courses
- Platform-wide analytics
- Revenue tracking
- User management

### 🤖 AI Features (Groq LLM)
- Intelligent chatbot for student queries
- Personalized course recommendations
- Learning path suggestions
- Study tips and concept explanations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Groq API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Dharun2712/Online_Course_Registration_System.git
cd course_system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file with your credentials (see `.env.example` for template):
```
MONGO_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key_change_this_in_production
DATABASE_NAME=online_course_platform
```

5. **Initialize the database**
```bash
python scripts/db_init.py
```

This will create:
- Database indexes
- Sample users (admin, instructors, students)
- Sample courses

6. **Run the application**
```bash
python run.py
```

7. **Access the platform**
```
http://localhost:5000
```

## 👥 Sample Credentials

### Admin
- **Email:** admin@coursehub.com
- **Password:** Admin@123

### Instructor
- **Email:** sarah@coursehub.com
- **Password:** Instructor@123

### Student
- **Email:** john@student.com
- **Password:** Student@123

## 📁 Project Structure

```
course_system/
│
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   │
│   ├── models/                  # MongoDB models
│   │   ├── user_model.py
│   │   ├── course_model.py
│   │   ├── enrollment_model.py
│   │   ├── progress_model.py
│   │   └── payment_model.py
│   │
│   ├── routes/                  # API endpoints
│   │   ├── auth_routes.py
│   │   ├── student_routes.py
│   │   ├── instructor_routes.py
│   │   ├── admin_routes.py
│   │   └── payment_routes.py
│   │
│   ├── services/                # Business logic & AI
│   │   ├── auth_service.py
│   │   ├── course_service.py
│   │   ├── enrollment_service.py
│   │   ├── chatbot_service.py
│   │   └── recommendation_service.py
│   │
│   └── utils/                   # Utilities
│       ├── jwt_helper.py
│       ├── password_hash.py
│       ├── validators.py
│       └── logger.py
│
├── templates/                   # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── course.html
│   ├── student_dashboard.html
│   ├── instructor_dashboard.html
│   └── admin_dashboard.html
│
├── static/
│   └── js/
│       └── api-client.js        # Frontend API client
│
├── scripts/
│   └── db_init.py               # Database initialization
│
├── requirements.txt
├── .env
├── run.py
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile

### Student
- `GET /api/student/courses` - Browse courses
- `POST /api/student/enroll` - Enroll in course
- `GET /api/student/my-courses` - Get enrolled courses
- `POST /api/student/chatbot` - AI chatbot
- `GET /api/student/recommendations` - AI recommendations

### Instructor
- `GET /api/instructor/courses` - Get instructor courses
- `POST /api/instructor/courses` - Create course
- `PUT /api/instructor/courses/:id` - Update course
- `POST /api/instructor/courses/:id/publish` - Publish course

### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/courses/pending` - Get pending courses
- `POST /api/admin/courses/:id/approve` - Approve course
- `GET /api/admin/statistics` - Platform statistics

### Payment
- `POST /api/payment/demo` - Demo payment processing
- `GET /api/payment/my-payments` - Get student payments

## 🤖 AI Integration

The platform uses **Groq AI (Llama 3.3-70B)** for:

1. **Chatbot Service** - Answers student questions about courses, provides study tips
2. **Recommendation Service** - Personalized course recommendations based on user profile
3. **Learning Path Generator** - Creates structured learning paths for career goals

## 🔐 Security Features

- JWT-based authentication
- Role-based access control (Student, Instructor, Admin)
- Password hashing with Werkzeug
- Input validation and sanitization
- Protected API endpoints

## 💳 Payment System

Demo payment implementation included. In production, integrate with:
- Stripe
- PayPal
- Razorpay
- etc.

## 📊 Features Implemented

✅ User authentication and authorization  
✅ Course management (CRUD)  
✅ Enrollment system  
✅ Progress tracking  
✅ Demo payment processing  
✅ AI chatbot (Groq LLM)  
✅ AI course recommendations  
✅ Learning analytics  
✅ Admin dashboard  
✅ Instructor dashboard  
✅ Student dashboard  
✅ Role-based access control  
✅ RESTful API  
✅ MongoDB integration  

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Database:** MongoDB Atlas
- **AI:** Groq API (Llama 3.3-70B)
- **Authentication:** JWT
- **Frontend:** HTML, CSS, JavaScript
- **Security:** Werkzeug, JWT

## 📝 Environment Setup Notes

- MongoDB is hosted on **MongoDB Atlas** (cloud)
- Groq API key is configured for AI features
- Application runs on `localhost:5000` by default
- All sample data is created automatically with `db_init.py`

## 🔧 Development

To add new features:

1. Create model in `app/models/`
2. Create service in `app/services/`
3. Create routes in `app/routes/`
4. Register blueprint in `app/__init__.py`

## 📖 API Documentation

For detailed API documentation, see the route files in `app/routes/`. Each endpoint includes:
- Method
- Authentication requirements
- Request/Response format
- Role requirements

## 🙏 Credits

Developed by **Dharun2712**  
GitHub: https://github.com/Dharun2712/Online_Course_Registration_System

## 📄 License

This project is for educational purposes.

---

**Happy Learning! 🎓**
