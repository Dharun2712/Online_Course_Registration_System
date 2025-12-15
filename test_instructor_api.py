"""
Test instructor dashboard API endpoint
"""
import requests
import json

# First, login as instructor
login_url = "http://localhost:5000/api/auth/login"
login_data = {
    "email": "instructor@gmail.com",
    "password": "123456"
}

print("=== Logging in as instructor ===")
response = requests.post(login_url, json=login_data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    token = result.get('token')
    print(f"✅ Login successful")
    print(f"User: {result.get('user', {}).get('name')}")
    print(f"Role: {result.get('user', {}).get('role')}")
    print(f"Token: {token[:20]}...")
    
    # Now test dashboard endpoint
    print("\n=== Testing Dashboard Endpoint ===")
    dashboard_url = "http://localhost:5000/api/instructor/dashboard"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    dashboard_response = requests.get(dashboard_url, headers=headers)
    print(f"Status: {dashboard_response.status_code}")
    
    if dashboard_response.status_code == 200:
        data = dashboard_response.json()
        print(f"✅ Dashboard data retrieved")
        print(f"Success: {data.get('success')}")
        print(f"Courses count: {len(data.get('courses', []))}")
        print(f"Analytics: {data.get('analytics', {})}")
        
        if data.get('courses'):
            print("\n=== Course Details ===")
            for course in data.get('courses', []):
                print(f"Title: {course.get('title')}")
                print(f"ID: {course.get('_id')}")
                print(f"Enrolled: {course.get('enrolled_count', 0)}")
                print(f"Price: ${course.get('price', 0)}")
                print("-" * 50)
        else:
            print("⚠️ No courses returned")
            print(f"Full response: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Failed to get dashboard data")
        print(f"Response: {dashboard_response.text}")
else:
    print(f"❌ Login failed: {response.text}")
