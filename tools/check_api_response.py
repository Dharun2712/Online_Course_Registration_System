import requests
import json

# Login as student
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'email': 'dharunkumarm2005@gmail.com',
    'password': 'dharun'
})

if login_response.status_code == 200:
    token = login_response.json()['token']
    
    # Get exams
    exams_response = requests.get(
        'http://localhost:5000/api/student/exams',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if exams_response.status_code == 200:
        data = exams_response.json()
        print("=== API RESPONSE ===")
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"Failed to get exams: {exams_response.status_code}")
        print(exams_response.text)
else:
    print(f"Login failed: {login_response.status_code}")
    print(login_response.text)
