"""
Test login API directly
"""

import requests
import json

# Test Admin Login
print("Testing Admin Login...")
response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={
        'email': 'admin@gmail.com',
        'password': 'admin@123'
    },
    headers={'Content-Type': 'application/json'}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*60 + "\n")

# Test Instructor Login
print("Testing Instructor Login...")
response = requests.post(
    'http://localhost:5000/api/auth/login',
    json={
        'email': 'instructor@gmail.com',
        'password': 'instructor@123'
    },
    headers={'Content-Type': 'application/json'}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
