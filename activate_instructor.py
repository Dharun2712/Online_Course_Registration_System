"""
Script to activate the instructor account
"""
from db_connection import get_database

try:
    # Connect to MongoDB
    db = get_database(allow_mutation=True)
    
    # Activate instructor account
    result = db.users.update_one(
        {'email': 'instructor@gmail.com'},
        {'$set': {'is_active': True}}
    )
    
    if result.matched_count > 0:
        print(f"✅ Account activated successfully!")
        print(f"   Modified: {result.modified_count} document(s)")
        
        # Show current status
        user = db.users.find_one({'email': 'instructor@gmail.com'}, {'name': 1, 'email': 1, 'is_active': 1})
        if user:
            print(f"\n📋 Current Status:")
            print(f"   Name: {user.get('name')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Active: {user.get('is_active', False)}")
    else:
        print("❌ User not found with email: instructor@gmail.com")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
