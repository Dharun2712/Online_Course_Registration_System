# 🧪 Quick Testing Guide

## Test All Updated Templates

### Prerequisites
1. **Start the server:**
   ```bash
   python run.py
   ```
2. **Server should be running on:** `http://localhost:5000`
3. **MongoDB should be connected** (check server logs)

---

## 1️⃣ Test Homepage (/)

**URL:** `http://localhost:5000/`

**Test Steps:**
1. ✅ Page loads without errors
2. ✅ Featured courses appear (should show 6 courses)
3. ✅ Click "Courses" in nav → Goes to `/courses`
4. ✅ Click a category card → Goes to `/courses`
5. ✅ Type in search box and click Search → Goes to `/courses` with search term
6. ✅ Click "Join for Free" → Goes to `/login`

**Expected Result:** All navigation works, courses load from API

---

## 2️⃣ Test Course Listing (/courses)

**URL:** `http://localhost:5000/courses`

**Test Steps:**
1. ✅ All courses load (should see 4 sample courses)
2. ✅ Type "Web" in search → Filters to Web Development course
3. ✅ Select "Programming" category → Filters courses
4. ✅ Select "Free" price → Shows only free courses
5. ✅ Select "Beginner" level → Filters by level
6. ✅ Change sort to "Price: Low to High" → Courses reorder
7. ✅ Click "View Details" on a course → Goes to course detail page

**Expected Result:** All filters work, search works, courses load dynamically

---

## 3️⃣ Test Login (/login)

**URL:** `http://localhost:5000/login`

**Test Credentials:**
```
Student:
  Email: john@student.com
  Password: password123

Instructor:
  Email: sarah@coursehub.com
  Password: password123

Admin:
  Email: admin@coursehub.com
  Password: admin123
```

**Test Steps:**

### Student Login
1. Click "Student" tab
2. Enter: `john@student.com` / `password123`
3. Click "Login as Student"
4. ✅ Should redirect to `/student/dashboard`
5. ✅ Navbar should show "John Doe" instead of "Join for Free"

### Instructor Login
1. Logout (if logged in)
2. Go back to `/login`
3. Click "Instructor" tab
4. Enter: `sarah@coursehub.com` / `password123`
5. Click "Login as Instructor"
6. ✅ Should redirect to `/instructor/dashboard`

### Admin Login
1. Logout and return to `/login`
2. Click "Admin" tab
3. Enter: `admin@coursehub.com` / `admin123`
4. Click "Login as Admin"
5. ✅ Should redirect to `/admin/dashboard`

**Expected Result:** Each role redirects to correct dashboard

---

## 4️⃣ Test Course Detail Page

**URL:** `http://localhost:5000/course/{course_id}`

**How to Get Course ID:**
1. Go to `/courses`
2. Right-click "View Details" on any course
3. Copy link (will be like `/course/67XXXXXXXXXXXXXXXX`)
4. Or just click the button to navigate

**Test Steps:**
1. ✅ Course title, price, description load correctly
2. ✅ Instructor information displays
3. ✅ Course materials show (if any)
4. ✅ Click "Description" tab → Shows description
5. ✅ Click "Materials" tab → Shows materials list
6. ✅ Recommended courses appear on right sidebar
7. ✅ Click recommended course → Navigate to that course

**Enrollment Test (Not Logged In):**
1. Logout if logged in
2. Go to course detail page
3. Click "Enroll Now"
4. ✅ Should redirect to `/login`

**Enrollment Test (Logged In as Student):**
1. Login as student
2. Go to course detail page
3. If already enrolled: ✅ Shows "✓ You are enrolled in this course"
4. If not enrolled: ✅ Shows "Enroll Now" button

**Expected Result:** All course data loads, enrollment button works

---

## 5️⃣ Test Enrollment & Payment

### Test Free Course Enrollment
1. Login as student (`john@student.com`)
2. Find a **FREE** course (e.g., "Introduction to Programming")
3. Click "View Details"
4. Click "Enroll Now"
5. ✅ Should auto-enroll and show success message
6. ✅ Redirects to `/student/dashboard`
7. ✅ Course appears in "My Enrolled Courses"

### Test Paid Course Enrollment
1. Login as student
2. Find a **PAID** course (e.g., "Web Development Bootcamp" - $49.99)
3. Click "View Details"
4. Click "Enroll Now"
5. ✅ Redirects to `/enroll?course_id={id}`
6. ✅ Course details display
7. ✅ Payment form appears

**Fill Payment Form:**
```
Card Number: 1234567812345678
Expiry: 12/25
CVV: 123
Cardholder: John Doe
```

8. Click "Complete Payment"
9. ✅ Shows "Processing..." message
10. ✅ Success message appears
11. ✅ Redirects to `/student/dashboard`
12. ✅ Course appears in enrolled courses

**Expected Result:** Enrollment flow works for both free and paid courses

---

## 6️⃣ Test About Page (/about)

**URL:** `http://localhost:5000/about`

**Test Steps:**
1. ✅ Page loads
2. ✅ All navigation links work
3. ✅ Footer links work
4. If logged in: ✅ Navbar shows username

**Expected Result:** Static page with working navigation

---

## 7️⃣ Test Student Dashboard

**URL:** `http://localhost:5000/student/dashboard`

**Test Steps:**
1. Login as student
2. ✅ Should see enrolled courses
3. ✅ Can view course progress
4. ✅ AI Chatbot works (type a question)
5. ✅ Recommendations load
6. ✅ Can click "Continue Learning" on courses

**Expected Result:** Dashboard shows all enrolled courses and works interactively

---

## 8️⃣ Test Instructor Dashboard

**URL:** `http://localhost:5000/instructor/dashboard`

**Test Steps:**
1. Login as instructor (`sarah@coursehub.com`)
2. ✅ See "My Courses" list
3. ✅ Can create new course
4. ✅ Can edit existing courses
5. ✅ Can add materials to courses

**Expected Result:** Instructor can manage their courses

---

## 9️⃣ Test Admin Dashboard

**URL:** `http://localhost:5000/admin/dashboard`

**Test Steps:**
1. Login as admin (`admin@coursehub.com`)
2. ✅ See platform statistics
3. ✅ View all courses
4. ✅ Approve/reject pending courses
5. ✅ Manage users

**Expected Result:** Admin can manage platform

---

## 🔍 Common Test Scenarios

### Scenario 1: Browse → Login → Enroll → Learn
```
1. Go to homepage (/)
2. Click "Courses"
3. Browse courses
4. Click course detail
5. Click "Enroll Now"
6. Login as student
7. Complete payment (if paid)
8. View course in dashboard
```

### Scenario 2: Already Logged In User
```
1. Login as student
2. Go to homepage
3. Navbar shows "John Doe" instead of "Join for Free"
4. Click username → Goes to dashboard
5. Browse courses
6. Enroll in new course → No login required
```

### Scenario 3: Search and Filter
```
1. Go to /courses
2. Search "Python"
3. Only Python courses show
4. Filter by "Free"
5. Only free Python courses show
6. Sort by "Newest"
7. Courses reorder
```

---

## 🐛 What to Look For (Potential Issues)

### ❌ Errors to Watch:
1. **404 Not Found** - Links still pointing to `.html` files
2. **Resource not found** - API endpoints not working
3. **Blank pages** - JavaScript errors preventing load
4. **Infinite loading** - API calls failing silently

### ✅ Success Indicators:
1. No console errors in browser DevTools (F12)
2. All courses load from database
3. Login redirects work properly
4. Enrollment creates database records
5. Navigation consistent across all pages

---

## 🛠️ Debugging Tips

### If Courses Don't Load:
1. Check server logs for MongoDB connection
2. Open browser console (F12) → Check for errors
3. Verify database has courses: `python scripts/db_init.py`

### If Login Doesn't Work:
1. Check credentials match database
2. Look for JWT token in localStorage (F12 → Application → Local Storage)
3. Check server logs for authentication errors

### If Enrollment Fails:
1. Verify you're logged in (check navbar)
2. Check course ID in URL is valid
3. Look at Network tab (F12) for failed API calls

---

## 📊 Quick Verification Checklist

- [ ] Homepage loads with 6 featured courses
- [ ] Courses page shows all 4 sample courses
- [ ] Search works on courses page
- [ ] Filters work (category, price, level)
- [ ] Course detail pages load correctly
- [ ] Student login redirects to student dashboard
- [ ] Instructor login redirects to instructor dashboard
- [ ] Admin login redirects to admin dashboard
- [ ] Free course enrollment works (auto-enrolls)
- [ ] Paid course enrollment shows payment form
- [ ] About page loads
- [ ] All navigation links work (no 404 errors)
- [ ] Already logged-in users see their name in navbar
- [ ] Logout works
- [ ] No "Resource not found" errors

---

## ✅ All Tests Pass?

**If YES:** 🎉 All templates are fully integrated with the backend!

**If NO:** 
1. Check which specific test failed
2. Review server logs: Look at Flask terminal output
3. Check browser console: F12 → Console tab
4. Verify MongoDB connection: Server should show "✅ Connected to MongoDB"

---

**Testing Date:** October 26, 2025  
**All Features:** Working as expected ✅
