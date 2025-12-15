"""
Test the instructor API to see what it returns
"""
import requests
import json

# First, login as instructor to get a token
print("=" * 60)
print("TESTING INSTRUCTOR API")
print("=" * 60)

# Step 1: Login
print("\n1. Logging in as instructor...")
login_data = {
    "email": "instructor@gmail.com",
    "password": "123456"
}

try:
    response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Success: {data.get('success')}")
        
        if data.get('success') and data.get('token'):
            token = data['token']
            user = data.get('user', {})
            print(f"   Token: {token[:30]}...")
            print(f"   User: {user.get('name')} ({user.get('role')})")
            
            # Step 2: Call dashboard API
            print("\n2. Calling /api/instructor/dashboard...")
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            dashboard_response = requests.get('http://localhost:5000/api/instructor/dashboard', headers=headers)
            print(f"   Status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print(f"\n3. Dashboard Data:")
                print(f"   Success: {dashboard_data.get('success')}")
                print(f"   Courses count: {len(dashboard_data.get('courses', []))}")
                
                if dashboard_data.get('courses'):
                    print(f"\n4. Courses:")
                    for idx, course in enumerate(dashboard_data['courses'], 1):
                        print(f"\n   Course {idx}:")
                        print(f"      Title: {course.get('title')}")
                        print(f"      ID: {course.get('_id')}")
                        print(f"      Published: {course.get('is_published')}")
                        print(f"      Enrolled Count: {course.get('enrolled_count')}")
                        print(f"      Price: ${course.get('price', 0)}")
                else:
                    print("   ⚠️ No courses in response")
                    print(f"   Full response: {json.dumps(dashboard_data, indent=2)}")
            else:
                print(f"   ❌ Error: {dashboard_response.text}")
        else:
            print(f"   ❌ Login failed: {data}")
    else:
        print(f"   ❌ HTTP Error: {response.text}")
        
except Exception as e:
    print(f"   💥 Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
