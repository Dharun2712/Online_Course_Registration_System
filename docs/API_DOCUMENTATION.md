# 📡 CourseHub API Documentation

Base URL: `http://localhost:5000/api`

All endpoints except `/auth/register` and `/auth/login` require JWT authentication.

## 🔐 Authentication

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Password@123",
  "role": "student"  // student, instructor, or admin
}

Response:
{
  "success": true,
  "message": "Registration successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "Password@123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }
}
```

### Get Profile
```http
GET /auth/profile
Authorization: Bearer {token}

Response:
{
  "success": true,
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student",
    "enrolled_courses": [],
    "created_at": "2024-01-01T00:00:00.000Z"
  }
}
```

---

## 🎓 Student Endpoints

### Browse Courses
```http
GET /student/courses?page=1&per_page=12&search=python
Authorization: Bearer {token}

Response:
{
  "success": true,
  "courses": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "title": "Python Programming",
      "description": "Learn Python from scratch",
      "price": 49.99,
      "level": "Beginner",
      "tags": ["Python", "Programming"],
      "rating": 4.5,
      "total_enrollments": 1250
    }
  ],
  "page": 1,
  "per_page": 12
}
```

### Get Course Details
```http
GET /student/courses/{course_id}
Authorization: Bearer {token}

Response:
{
  "success": true,
  "course": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Python Programming",
    "description": "Complete Python course",
    "instructor_id": "507f1f77bcf86cd799439012",
    "price": 49.99,
    "materials": [...],
    "students": [...],
    "rating": 4.5
  }
}
```

### Enroll in Course
```http
POST /student/enroll
Authorization: Bearer {token}
Content-Type: application/json

{
  "course_id": "507f1f77bcf86cd799439011",
  "payment_id": "507f1f77bcf86cd799439013"  // Optional for free courses
}

Response:
{
  "success": true,
  "message": "Enrollment successful"
}
```

### Get My Courses
```http
GET /student/my-courses?status=active
Authorization: Bearer {token}

Response:
{
  "success": true,
  "enrollments": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "course_id": "507f1f77bcf86cd799439012",
      "progress": 45,
      "status": "active",
      "enrolled_at": "2024-01-01T00:00:00.000Z",
      "course": { ... }
    }
  ]
}
```

### Update Progress
```http
POST /student/progress/{course_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "progress_percent": 75
}

Response:
{
  "success": true,
  "message": "Progress updated"
}
```

### AI Chatbot
```http
POST /student/chatbot
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "What courses do you recommend for web development?",
  "context": {
    "current_course": "Python Programming"
  }
}

Response:
{
  "success": true,
  "response": "For web development, I recommend starting with..."
}
```

### Get AI Recommendations
```http
GET /student/recommendations?interests=web&interests=python&skill_level=beginner
Authorization: Bearer {token}

Response:
{
  "success": true,
  "recommendations": [
    "1. Complete Web Development Bootcamp - Perfect for beginners",
    "2. Python for Web Development - Learn Flask and Django",
    "3. JavaScript Fundamentals - Essential for web development"
  ]
}
```

---

## 👨‍🏫 Instructor Endpoints

### Get My Courses
```http
GET /instructor/courses
Authorization: Bearer {token}

Response:
{
  "success": true,
  "courses": [...]
}
```

### Create Course
```http
POST /instructor/courses
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Advanced Python Programming",
  "description": "Master advanced Python concepts",
  "price": 99.99,
  "tags": ["Python", "Advanced", "Programming"],
  "duration": "10 weeks",
  "level": "Advanced"
}

Response:
{
  "success": true,
  "message": "Course created successfully",
  "course_id": "507f1f77bcf86cd799439011"
}
```

### Update Course
```http
PUT /instructor/courses/{course_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Title",
  "price": 79.99
}

Response:
{
  "success": true,
  "message": "Course updated successfully"
}
```

### Publish Course
```http
POST /instructor/courses/{course_id}/publish
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "Course published successfully"
}
```

### Add Course Material
```http
POST /instructor/courses/{course_id}/materials
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Introduction to Variables",
  "type": "video",
  "url": "https://example.com/video.mp4",
  "order": 1,
  "duration": "15 minutes"
}

Response:
{
  "success": true,
  "message": "Material added successfully"
}
```

### Get Course Students
```http
GET /instructor/courses/{course_id}/students
Authorization: Bearer {token}

Response:
{
  "success": true,
  "students": [
    {
      "student_id": "507f1f77bcf86cd799439011",
      "progress": 65,
      "enrolled_at": "2024-01-01T00:00:00.000Z",
      "student": {
        "name": "John Doe",
        "email": "john@example.com"
      }
    }
  ]
}
```

### Get Statistics
```http
GET /instructor/statistics
Authorization: Bearer {token}

Response:
{
  "success": true,
  "statistics": {
    "total_courses": 5,
    "published_courses": 3,
    "total_enrollments": 150,
    "average_rating": 4.5
  }
}
```

---

## 👑 Admin Endpoints

### Get All Users
```http
GET /admin/users?role=student&page=1&per_page=50
Authorization: Bearer {token}

Response:
{
  "success": true,
  "users": [...],
  "page": 1,
  "per_page": 50
}
```

### Deactivate User
```http
DELETE /admin/users/{user_id}
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "User deactivated"
}
```

### Get Pending Courses
```http
GET /admin/courses/pending
Authorization: Bearer {token}

Response:
{
  "success": true,
  "courses": [...]
}
```

### Approve Course
```http
POST /admin/courses/{course_id}/approve
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "Course approved"
}
```

### Reject Course
```http
POST /admin/courses/{course_id}/reject
Authorization: Bearer {token}
Content-Type: application/json

{
  "reason": "Does not meet quality standards"
}

Response:
{
  "success": true,
  "message": "Course rejected"
}
```

### Get Platform Statistics
```http
GET /admin/statistics
Authorization: Bearer {token}

Response:
{
  "success": true,
  "statistics": {
    "users": {
      "total": 1500,
      "students": 1200,
      "instructors": 50
    },
    "courses": {
      "total_courses": 200,
      "published_courses": 150
    },
    "enrollments": {
      "total_enrollments": 5000,
      "active_enrollments": 3000
    },
    "revenue": {
      "total_revenue": 50000.00,
      "total_transactions": 1000
    }
  }
}
```

---

## 💳 Payment Endpoints

### Process Demo Payment
```http
POST /payment/demo
Authorization: Bearer {token}
Content-Type: application/json

{
  "course_id": "507f1f77bcf86cd799439011"
}

Response:
{
  "success": true,
  "message": "Payment processed successfully (Demo)",
  "payment": {
    "_id": "507f1f77bcf86cd799439013",
    "transaction_id": "TXN202410261234567890",
    "amount": 49.99,
    "status": "completed"
  }
}
```

### Get My Payments
```http
GET /payment/my-payments
Authorization: Bearer {token}

Response:
{
  "success": true,
  "payments": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "transaction_id": "TXN202410261234567890",
      "course_id": "507f1f77bcf86cd799439012",
      "amount": 49.99,
      "status": "completed",
      "created_at": "2024-01-01T00:00:00.000Z",
      "course": { ... }
    }
  ]
}
```

### Verify Payment
```http
GET /payment/verify/{course_id}
Authorization: Bearer {token}

Response:
{
  "success": true,
  "has_paid": true
}
```

---

## 🔑 Authentication Header

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "error": "Token is missing"
}
```

### 403 Forbidden
```json
{
  "error": "Unauthorized. Admin role required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## 📝 Notes

- All timestamps are in UTC
- Pagination starts at page 1
- Default page size is 12 for courses, 50 for users
- JWT tokens expire after 24 hours
- Demo payments are automatically approved
- Course approval required before publishing

---

**For more details, see the source code in `app/routes/`**
