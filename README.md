<div align="center">

# 🎓 CourseHub - Online Learning Platform

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=6366F1&center=true&vCenter=true&width=940&lines=Welcome+to+CourseHub!;Learn+Anything%2C+Anytime%2C+Anywhere;AI-Powered+Learning+Experience" alt="Typing SVG" />

[![JavaScript](https://img.shields.io/badge/JavaScript-ES2022-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4.x-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![AI Powered](https://img.shields.io/badge/AI-Groq_Llama-FF6B6B?style=for-the-badge&logo=ai&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**A comprehensive online course registration and learning management system with AI-powered features**

[🚀 Getting Started](#-quick-start) •
[📖 Documentation](#-documentation) •
[✨ Features](#-features) •
[🏗️ Architecture](#-system-architecture) •
[🤝 Contributing](#-contributing)

---

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [User Flow](#-user-flow)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

<div align="center">

```ascii
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   CourseHub - Transform Your Learning Journey               ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       ║
║                                                              ║
║   🎯 Smart Course Recommendations                           ║
║   🤖 AI-Powered Learning Assistant                          ║
║   📊 Real-time Progress Tracking                            ║
║   🎓 Digital Certificates                                    ║
║   💳 Secure Payment Integration                             ║
║   📱 Responsive Design                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

CourseHub is a modern, full-featured Learning Management System (LMS) that bridges the gap between learners and quality education. Built with JavaScript and a Node.js backend, it provides an intuitive platform for students to discover courses, track their progress, and achieve their learning goals with the help of AI-powered assistance.

### 🎯 Key Highlights

- **🧠 AI Integration**: Powered by Groq's Llama 3.3-70B model for intelligent course recommendations and chatbot assistance
- **👥 Multi-Role System**: Separate dashboards and workflows for Students, Instructors, and Admins
- **📈 Analytics**: Comprehensive analytics and reporting for all user types
- **🔐 Secure**: JWT-based authentication with password hashing
- **⚡ Fast**: Optimized database queries and caching strategies
- **📱 Responsive**: Mobile-first design approach

---

## ✨ Features

<div align="center">

### 🎓 For Students

| Feature | Description |
|---------|-------------|
| 🔍 **Course Discovery** | Browse and search through extensive course catalog with advanced filters |
| 📚 **Enrollment Management** | Easy one-click enrollment with payment processing |
| 📊 **Progress Tracking** | Visual progress indicators and learning analytics |
| 🤖 **AI Chatbot** | 24/7 intelligent assistant for course-related queries |
| 💡 **Smart Recommendations** | Personalized course suggestions based on learning history |
| 🎓 **Certificates** | Downloadable certificates upon course completion |
| 💬 **Discussion Forums** | Engage with peers and instructors |
| 📱 **Mobile Learning** | Learn on-the-go with responsive design |

### 👨‍🏫 For Instructors

| Feature | Description |
|---------|-------------|
| ✍️ **Course Creation** | Intuitive course builder with rich content support |
| 📹 **Content Management** | Upload videos, documents, and interactive materials |
| 👥 **Student Management** | Track enrollments and student progress |
| 📊 **Analytics Dashboard** | Detailed insights on course performance |
| 💰 **Revenue Tracking** | Monitor earnings and payment history |
| ✅ **Exam Management** | Create and grade assessments |
| 📆 **Live Classes** | Schedule and conduct live sessions |
| 📧 **Communication Tools** | Announcements and direct messaging |

### 👑 For Administrators

| Feature | Description |
|---------|-------------|
| 🔐 **User Management** | Complete control over user accounts and permissions |
| ✅ **Course Approval** | Review and approve instructor-created courses |
| 📊 **Platform Analytics** | System-wide statistics and performance metrics |
| 💳 **Payment Management** | Transaction monitoring and financial reports |
| 🛡️ **Content Moderation** | Ensure quality and compliance |
| ⚙️ **System Configuration** | Platform settings and customization |
| 📈 **Growth Metrics** | User acquisition and retention analytics |
| 🔔 **Notification System** | Automated alerts and announcements |

</div>

---

## 🏗️ System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile Browser]
    end
    
    subgraph "Presentation Layer"
        C[HTML Templates]
        D[JavaScript/API Client]
        E[CSS/Responsive Design]
    end
    
    subgraph "Application Layer"
        F[Flask Application]
        G[Route Handlers]
        H[Business Logic Services]
    end
    
    subgraph "Service Layer"
        I[Auth Service]
        J[Course Service]
        K[Enrollment Service]
        L[Payment Service]
        M[AI Chatbot Service]
        N[Analytics Service]
    end
    
    subgraph "Data Layer"
        O[(MongoDB)]
        P[User Collection]
        Q[Course Collection]
        R[Enrollment Collection]
        S[Payment Collection]
    end
    
    subgraph "External Services"
        T[Groq AI API]
        U[Payment Gateway]
        V[Email Service]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> G
    G --> H
    H --> I
    H --> J
    H --> K
    H --> L
    H --> M
    H --> N
    I --> O
    J --> O
    K --> O
    L --> O
    M --> T
    L --> U
    N --> V
    O --> P
    O --> Q
    O --> R
    O --> S
    
    style A fill:#6366f1,stroke:#4f46e5,stroke-width:2px,color:#fff
    style B fill:#6366f1,stroke:#4f46e5,stroke-width:2px,color:#fff
    style F fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style O fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    style T fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
```

### Component Architecture

```mermaid
graph LR
    subgraph "Frontend Components"
        A1[Landing Page]
        A2[Authentication]
        A3[Dashboard]
        A4[Course Catalog]
        A5[Learning Interface]
        A6[Profile Management]
    end
    
    subgraph "Backend Services"
        B1[API Gateway]
        B2[Auth Service]
        B3[Course Service]
        B4[User Service]
        B5[AI Service]
        B6[Analytics Service]
    end
    
    subgraph "Data Models"
        C1[User Model]
        C2[Course Model]
        C3[Enrollment Model]
        C4[Progress Model]
        C5[Payment Model]
        C6[Certificate Model]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    A5 --> B1
    A6 --> B1
    
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B1 --> B5
    B1 --> B6
    
    B2 --> C1
    B3 --> C2
    B4 --> C3
    B5 --> C4
    B6 --> C5
    B6 --> C6
    
    style B1 fill:#8b5cf6,stroke:#7c3aed,stroke-width:3px,color:#fff
```

---

## 🔄 User Flow Diagrams

### Student Enrollment Flow

```mermaid
sequenceDiagram
    participant S as Student
    participant UI as Web Interface
    participant API as Flask API
    participant DB as MongoDB
    participant AI as Groq AI
    participant Pay as Payment Gateway
    
    S->>UI: Browse Courses
    UI->>API: GET /api/student/courses
    API->>DB: Query Courses
    DB-->>API: Return Courses
    API-->>UI: Course List
    UI-->>S: Display Courses
    
    S->>UI: View Course Details
    UI->>API: GET /api/student/course/{id}
    API->>DB: Fetch Course Details
    DB-->>API: Course Data
    API->>AI: Get Recommendations
    AI-->>API: Similar Courses
    API-->>UI: Course + Recommendations
    UI-->>S: Show Details
    
    S->>UI: Enroll in Course
    alt Paid Course
        UI->>Pay: Process Payment
        Pay-->>UI: Payment Success
    end
    UI->>API: POST /api/student/enroll
    API->>DB: Create Enrollment
    DB-->>API: Enrollment Created
    API-->>UI: Success Response
    UI-->>S: Show Success Message
    
    S->>UI: Access Course Content
    UI->>API: GET /api/student/learn/{courseId}
    API->>DB: Verify Enrollment
    DB-->>API: Access Granted
    API-->>UI: Course Materials
    UI-->>S: Display Learning Interface
```

### Instructor Course Creation Flow

```mermaid
sequenceDiagram
    participant I as Instructor
    participant UI as Web Interface
    participant API as Flask API
    participant DB as MongoDB
    participant Admin as Admin Panel
    
    I->>UI: Login to Dashboard
    UI->>API: POST /api/auth/login
    API->>DB: Verify Credentials
    DB-->>API: User Data
    API-->>UI: JWT Token
    UI-->>I: Show Dashboard
    
    I->>UI: Create New Course
    UI->>API: POST /api/instructor/course
    Note over API: Validate Course Data
    API->>DB: Save Course (pending)
    DB-->>API: Course ID
    API-->>UI: Course Created
    UI-->>I: Show Success
    
    Admin->>UI: Review Course
    UI->>API: GET /api/admin/pending-courses
    API->>DB: Fetch Pending Courses
    DB-->>API: Course List
    API-->>UI: Display Courses
    
    Admin->>UI: Approve Course
    UI->>API: PUT /api/admin/course/{id}/approve
    API->>DB: Update Course Status
    DB-->>API: Updated
    API-->>UI: Success
    
    Note over I: Receives Email Notification
    I->>UI: Check Dashboard
    UI-->>I: Course Now Active
```

### AI Chatbot Interaction Flow

```mermaid
sequenceDiagram
    participant S as Student
    participant UI as Chat Interface
    participant API as Flask API
    participant Cache as Redis Cache
    participant AI as Groq AI (Llama 3.3)
    participant DB as MongoDB
    
    S->>UI: Ask Question
    UI->>API: POST /api/student/chatbot
    
    API->>Cache: Check Cache
    alt Cache Hit
        Cache-->>API: Cached Response
        API-->>UI: Return Answer
    else Cache Miss
        API->>DB: Fetch Course Context
        DB-->>API: Course Data
        API->>AI: Generate Response
        Note over AI: Llama 3.3-70B Processing
        AI-->>API: AI Response
        API->>Cache: Store Response
        API-->>UI: Return Answer
    end
    
    UI-->>S: Display Answer
    
    opt Follow-up Question
        S->>UI: Ask Follow-up
        Note over API: Context Maintained
        UI->>API: POST /api/student/chatbot
        API->>AI: Process with Context
        AI-->>API: Contextual Response
        API-->>UI: Return Answer
        UI-->>S: Display Answer
    end
```

---

## 🛢️ Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ ENROLLMENT : creates
    USER ||--o{ COURSE : instructs
    USER ||--o{ PAYMENT : makes
    COURSE ||--o{ ENROLLMENT : has
    COURSE ||--o{ MODULE : contains
    COURSE ||--o{ EXAM : includes
    ENROLLMENT ||--o{ PROGRESS : tracks
    ENROLLMENT ||--o{ CERTIFICATE : generates
    ENROLLMENT ||--o{ PAYMENT : requires
    MODULE ||--o{ CONTENT : contains
    EXAM ||--o{ EXAM_SUBMISSION : has
    
    USER {
        ObjectId _id PK
        string email UK
        string password
        string name
        string role
        datetime created_at
        datetime updated_at
        boolean is_active
        string profile_picture
    }
    
    COURSE {
        ObjectId _id PK
        string title
        string description
        ObjectId instructor_id FK
        float price
        string category
        string level
        array tags
        string status
        int duration
        datetime created_at
        datetime updated_at
        int enrolled_count
        float rating
    }
    
    ENROLLMENT {
        ObjectId _id PK
        ObjectId student_id FK
        ObjectId course_id FK
        datetime enrolled_at
        string status
        float progress_percentage
        datetime completed_at
        boolean certificate_issued
    }
    
    PROGRESS {
        ObjectId _id PK
        ObjectId enrollment_id FK
        ObjectId module_id FK
        boolean completed
        datetime completed_at
        int time_spent
        array quiz_scores
    }
    
    PAYMENT {
        ObjectId _id PK
        ObjectId user_id FK
        ObjectId enrollment_id FK
        float amount
        string currency
        string payment_method
        string status
        datetime created_at
        string transaction_id
    }
    
    MODULE {
        ObjectId _id PK
        ObjectId course_id FK
        string title
        string description
        int order
        int duration
        array content_items
    }
    
    EXAM {
        ObjectId _id PK
        ObjectId course_id FK
        string title
        int duration
        int passing_score
        array questions
        datetime start_date
        datetime end_date
    }
    
    CERTIFICATE {
        ObjectId _id PK
        ObjectId enrollment_id FK
        string certificate_url
        datetime issued_at
        string certificate_id
    }
```

### Collection Indexes

```mermaid
graph TD
    subgraph "User Collection"
        U1[email: unique]
        U2[role: 1]
        U3[created_at: -1]
    end
    
    subgraph "Course Collection"
        C1[instructor_id: 1]
        C2[status: 1]
        C3[category: 1, level: 1]
        C4[title: text]
        C5[rating: -1]
    end
    
    subgraph "Enrollment Collection"
        E1[student_id: 1, course_id: 1]
        E2[status: 1]
        E3[enrolled_at: -1]
    end
    
    subgraph "Payment Collection"
        P1[user_id: 1]
        P2[transaction_id: unique]
        P3[created_at: -1]
    end
    
    style U1 fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style C1 fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
    style E1 fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    style P1 fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
```

---

## 🚀 Tech Stack

<div align="center">

### Backend Technologies

| Technology | Purpose | Version |
|:----------:|:-------:|:-------:|
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | Core Language | ES2022 |
| ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) | Runtime | 18+ |
| ![Express](https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white) | Web Framework | 4.x |
| ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white) | Database | 4.6+ |
| ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white) | Authentication | 2.8.0 |
| ![Groq](https://img.shields.io/badge/Groq_AI-FF6B6B?style=for-the-badge&logo=ai&logoColor=white) | AI Engine | Latest |

### Frontend Technologies

| Technology | Purpose |
|:----------:|:-------:|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | Structure |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | Styling |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | Interactivity |
| ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white) | UI Framework |

### Development Tools

| Tool | Purpose |
|:----:|:-------:|
| ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) | Version Control |
| ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) | IDE |
| ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) | API Testing |

</div>

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- ✅ Python 3.12 or higher
- ✅ MongoDB Atlas account (or local MongoDB)
- ✅ Groq API key ([Get it here](https://console.groq.com))
- ✅ Git

### Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Dharun2712/Online_Course_Registration_System.git
cd Online_Course_Registration_System
```

#### 2️⃣ Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 3️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/online_course_platform?retryWrites=true&w=majority
CUSTOMCONNSTR_MONGO_URI=
MONGO_DB_NAME=online_course_platform
DATABASE_NAME=online_course_platform

# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Security
SECRET_KEY=your_super_secret_key_change_in_production
JWT_SECRET_KEY=

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=true
PORT=3000
CORS_ORIGINS=
```

> 💡 **Tip:** Check `.env.example` for a template

#### 4️⃣ Initialize Database

```bash
python scripts/db_init.py
```

This script will:
- ✅ Create necessary database indexes
- ✅ Set up default admin user
- ✅ Create sample instructors and students
- ✅ Add demo courses

#### 5️⃣ Run the Application

```bash
python run.py
```

**Or use the quick start scripts:**

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### 6️⃣ Access the Platform

Open your browser and navigate to:

```
http://localhost:3000
```

---

## 👥 Default User Accounts

After initialization, use these credentials to explore different roles:

<div align="center">

| Role | Email | Password | Access Level |
|:----:|:-----:|:--------:|:------------:|
| 🔐 Admin | admin@coursehub.com | admin123 | Full Access |
| 👨‍🏫 Instructor | instructor@coursehub.com | instructor123 | Create/Manage Courses |
| 🎓 Student | student@coursehub.com | student123 | Browse/Enroll |

</div>

> ⚠️ **Security Note:** Change these passwords immediately in production!

---

## 📚 API Documentation

### Authentication Endpoints

```mermaid
graph LR
    A[Auth API] --> B[POST /api/auth/register]
    A --> C[POST /api/auth/login]
    A --> D[GET /api/auth/profile]
    A --> E[PUT /api/auth/profile]
    A --> F[POST /api/auth/logout]
    
    style A fill:#6366f1,stroke:#4f46e5,stroke-width:3px,color:#fff
    style B fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style C fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style D fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
    style E fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    style F fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
```

#### Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123",
  "role": "student"
}
```

**Response:**
```json
{
  "message": "Registration successful",
  "user": {
    "id": "60f1234567890abcdef12345",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "60f1234567890abcdef12345",
    "name": "John Doe",
    "role": "student"
  }
}
```

### Course Endpoints

```mermaid
graph TD
    A[Course API] --> B[Student Routes]
    A --> C[Instructor Routes]
    A --> D[Admin Routes]
    
    B --> B1[GET /api/student/courses]
    B --> B2[GET /api/student/course/:id]
    B --> B3[POST /api/student/enroll]
    B --> B4[GET /api/student/my-courses]
    
    C --> C1[POST /api/instructor/course]
    C --> C2[PUT /api/instructor/course/:id]
    C --> C3[DELETE /api/instructor/course/:id]
    C --> C4[GET /api/instructor/students]
    
    D --> D1[GET /api/admin/courses]
    D --> D2[PUT /api/admin/course/:id/approve]
    D --> D3[GET /api/admin/analytics]
    
    style A fill:#8b5cf6,stroke:#7c3aed,stroke-width:3px,color:#fff
    style B fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
    style C fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style D fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
```

### AI Chatbot Endpoint

```http
POST /api/student/chatbot
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "What are the prerequisites for Python course?",
  "course_id": "60f1234567890abcdef12345"
}
```

**Response:**
```json
{
  "response": "The Python for Beginners course has the following prerequisites:\n\n1. Basic computer skills\n2. No prior programming experience required\n3. Willingness to learn\n\nThis course is designed for absolute beginners and starts from the basics.",
  "timestamp": "2025-12-15T10:30:00Z"
}
```

> 📖 **Full API Documentation:** See [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for complete endpoint reference

---

## 📁 Project Structure

```
course_system/
│
├── 📄 server.js                       # Application entry point
├── 📄 package.json                    # Node dependencies
├── 📄 .env.example                    # Environment variables template
├── 📄 .gitignore                      # Git ignore rules
│
├── 📁 app/
│   ├── 📄 app.js                      # Express app setup
│   ├── 📄 config.js                   # Configuration management
│   │
│   ├── 📁 models/                    # Database models
│   │   ├── 📄 user_model.js          # User schema
│   │   ├── 📄 course_model.js        # Course schema
│   │   ├── 📄 enrollment_model.js    # Enrollment schema
│   │   ├── 📄 progress_model.js      # Progress tracking
│   │   ├── 📄 payment_model.js       # Payment records
│   │   ├── 📄 exam_model.js          # Exam schema
│   │   ├── 📄 certificate_model.js   # Certificate schema
│   │   ├── 📄 liveclass_model.js     # Live class schema
│   │   └── 📄 attendance_model.js    # Attendance records
│   │
│   ├── 📁 routes/                    # API endpoints
│   │   ├── 📄 auth_routes.js         # Authentication
│   │   ├── 📄 student_routes.js      # Student operations
│   │   ├── 📄 instructor_routes.js   # Instructor operations
│   │   ├── 📄 admin_routes.js        # Admin operations
│   │   ├── 📄 payment_routes.js      # Payment processing
│   │   └── 📄 ai_routes.js           # AI features
│   │
│   ├── 📁 services/                  # Business logic
│   │   ├── 📄 auth_service.js        # Authentication logic
│   │   ├── 📄 course_service.js      # Course management
│   │   ├── 📄 enrollment_service.js  # Enrollment logic
│   │   ├── 📄 payment_service.js     # Payment processing
│   │   ├── 📄 chatbot_service.js     # AI chatbot
│   │   ├── 📄 recommendation_service.js # AI recommendations
│   │   ├── 📄 analytics_service.js   # Analytics and reports
│   │   ├── 📄 certificate_service.js # Certificate generation
│   │   ├── 📄 exam_service.js        # Exam management
│   │   ├── 📄 liveclass_service.js   # Live class handling
│   │   └── 📄 attendance_service.js  # Attendance tracking
│   │
│   └── 📁 utils/                     # Helper functions
│       ├── 📄 jwt_helper.js          # JWT operations
│       ├── 📄 password_hash.js       # Password utilities
│       ├── 📄 validators.js          # Input validation
│       └── 📄 logger.js              # Logging configuration
│
├── 📁 templates/                     # HTML templates
│   ├── 📄 index.html                # Landing page
│   ├── 📄 login.html                # Login page
│   ├── 📄 courses.html              # Course catalog
│   ├── 📄 course_detail.html        # Course details
│   ├── 📄 course_learning.html      # Learning interface
│   ├── 📄 student_dashboard.html    # Student dashboard
│   ├── 📄 instructor_dashboard.html # Instructor dashboard
│   ├── 📄 admin_dashboard.html      # Admin dashboard
│   ├── 📄 payment.html              # Payment page
│   ├── 📄 certificate.html          # Certificate template
│   └── 📄 ...                       # Other templates
│
├── 📁 static/                        # Static assets
│   ├── 📁 js/                       # JavaScript files
│   │   └── 📄 api-client.js        # API client library
│   ├── 📁 css/                      # Stylesheets
│   ├── 📁 course_images/            # Course thumbnails
│   ├── 📁 certificate_templates/    # Certificate templates
│   └── 📁 uploads/                  # User uploads
│
├── 📁 scripts/                       # Utility scripts
│   └── 📄 db_init.js                # Database initialization
│
├── 📁 docs/                          # Documentation
│   ├── 📄 API_DOCUMENTATION.md      # API reference
│   ├── 📄 SETUP_GUIDE.md            # Setup instructions
│   ├── 📄 PROJECT_SUMMARY.md        # Project overview
│   └── 📄 ...                       # Other docs
│
├── 📁 tools/                         # Development tools
│   ├── 📄 seed_data.js              # Sample data generator
│   ├── 📄 db_inspect.js             # Database inspector
│   └── 📄 ...                       # Other tools
│
├── 📁 logs/                          # Application logs
├── 📁 certificates/                  # Generated certificates
└── 📁 tests/                         # Test files
```

---

## 🎨 Screenshots

<div align="center">

### Landing Page
> Modern, responsive landing page with hero section and featured courses

### Student Dashboard
> Personalized dashboard with progress tracking and AI recommendations

### Course Learning Interface
> Interactive learning environment with video content and quizzes

### Instructor Dashboard
> Comprehensive course management and analytics

### Admin Panel
> Platform-wide administration and analytics

</div>

> 📸 **Note:** Screenshots coming soon! The platform is fully functional and ready to use.

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py
```

### Manual Testing

Use the provided test scripts:

```bash
# Test API endpoints
python test_api.py

# Test authentication
python test_login.py

# Test instructor features
python test_instructor_api.py
```

### Test Users

The database initialization creates test users for each role:

- **Admin:** admin@coursehub.com / admin123
- **Instructor:** instructor@coursehub.com / instructor123
- **Student:** student@coursehub.com / student123

---

## 🚢 Deployment

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set MONGO_URI=your_mongodb_uri
heroku config:set GROQ_API_KEY=your_groq_key
heroku config:set SECRET_KEY=your_secret_key

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy to AWS / Azure / GCP

For Azure App Service, configure the application settings listed below and set the startup command to:

```text
gunicorn --bind=0.0.0.0:$PORT run:app
```

Required Azure settings:

```text
FLASK_ENV=production
FLASK_DEBUG=false
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/online_course_platform?retryWrites=true&w=majority
DATABASE_NAME=online_course_platform
MONGO_DB_NAME=online_course_platform
SECRET_KEY=<long-random-value>
JWT_SECRET_KEY=<optional-separate-jwt-secret>
GROQ_API_KEY=<optional-groq-key>
```

Set `MONGO_URI` as an App Service application setting. If using Azure Connection Strings instead, name it `MONGO_URI`; the application also accepts the generated `CUSTOMCONNSTR_MONGO_URI` variable. Use the existing database user and database; no initialization script runs during deployment.

In MongoDB Atlas, allow the App Service outbound IP addresses under Network Access. For a quick temporary test, Atlas can allow `0.0.0.0/0`, but a restricted list is preferred for production.

Test the deployment with `https://coursehub.azurewebsites.net/api/health`. A healthy response reports `"database": "connected"`. Test login with a `POST` request to `/api/auth/login` using an existing user; the response token is then sent as `Authorization: Bearer <token>`. View startup and application errors in App Service > Monitoring > Log stream.

Do not set `ALLOW_DB_INIT` or `ALLOW_DB_MUTATIONS` in Azure during normal deployments. The GitHub Actions workflow deploys on pushes to `main` and requires the repository secret `AZUREAPPSERVICE_PUBLISHPROFILE`.

### Docker Deployment

```bash
# Build image
docker build -t coursehub .

# Run container
docker run -p 5000:5000 --env-file .env coursehub
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report Bugs:** Found a bug? [Open an issue](https://github.com/Dharun2712/Online_Course_Registration_System/issues)
- 💡 **Feature Requests:** Have an idea? Share it with us!
- 📝 **Documentation:** Help improve our docs
- 💻 **Code:** Submit pull requests with improvements

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests (`python -m pytest`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write unit tests for new features

---

## 📊 Features Roadmap

```mermaid
gantt
    title CourseHub Development Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1 - Core
    User Authentication           :done, 2025-01-01, 2025-01-15
    Course Management            :done, 2025-01-16, 2025-02-01
    Enrollment System            :done, 2025-02-02, 2025-02-15
    
    section Phase 2 - AI
    Chatbot Integration          :done, 2025-02-16, 2025-03-01
    Recommendations Engine       :done, 2025-03-02, 2025-03-15
    
    section Phase 3 - Advanced
    Live Classes                 :active, 2025-03-16, 2025-04-01
    Mobile App                   :2025-04-02, 2025-05-01
    Advanced Analytics           :2025-05-02, 2025-06-01
    
    section Phase 4 - Enterprise
    Multi-tenancy                :2025-06-02, 2025-07-01
    Custom Branding              :2025-07-02, 2025-08-01
    API Marketplace              :2025-08-02, 2025-09-01
```

### Upcoming Features

- ✅ **Completed**
  - User authentication and authorization
  - Course creation and management
  - Enrollment and payment processing
  - AI-powered chatbot and recommendations
  - Progress tracking and certificates
  - Admin dashboard and analytics

- 🚧 **In Progress**
  - Live video streaming for classes
  - Mobile responsive improvements
  - Advanced analytics dashboard

- 📋 **Planned**
  - Mobile applications (iOS & Android)
  - Gamification features (badges, leaderboards)
  - Social learning features
  - Integration with Zoom/Google Meet
  - Multi-language support
  - Offline course downloads
  - Custom certificate designer
  - Affiliate marketing system

---

## 🔒 Security

### Security Features

- 🔐 **Password Hashing:** Werkzeug's secure password hashing
- 🎫 **JWT Tokens:** Stateless authentication
- 🛡️ **Input Validation:** Comprehensive input sanitization
- 🔒 **CORS Protection:** Configured CORS policies
- 📝 **Logging:** Security event logging
- 🚫 **Rate Limiting:** API rate limiting (coming soon)

### Reporting Security Issues

If you discover a security vulnerability, please email: security@coursehub.com

**Do not create public GitHub issues for security vulnerabilities.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Dharun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👥 Team

<div align="center">

### Developed with ❤️ by

**Dharun**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Dharun2712)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:dharun@example.com)

</div>

---

## 🌟 Support

If you find this project helpful, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 📢 **Sharing** with others

---

## 📞 Contact & Support

<div align="center">

### Need Help?

- 📧 **Email:** support@coursehub.com
- 💬 **Discord:** [Join our community](https://discord.gg/coursehub)
- 🐛 **Issues:** [GitHub Issues](https://github.com/Dharun2712/Online_Course_Registration_System/issues)
- 📖 **Docs:** [Full Documentation](docs/README.md)

</div>

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Amazing Python web framework
- [MongoDB](https://www.mongodb.com/) - Flexible NoSQL database
- [Groq](https://groq.com/) - Lightning-fast AI inference
- [Bootstrap](https://getbootstrap.com/) - Responsive UI components
- All contributors and supporters of this project

---

<div align="center">

### ⚡ Built with Modern Technologies for Modern Learning

**[⬆ Back to Top](#-coursehub---online-learning-platform)**

---

Made with ❤️ and ☕ by developers who believe in accessible education for all

**© 2025 CourseHub. All Rights Reserved.**

</div>
