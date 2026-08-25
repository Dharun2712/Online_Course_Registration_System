"""
Script to update course prices to Indian Rupees
Average prices: ₹500 - ₹2000
"""
from db_connection import get_database

try:
    # Connect to MongoDB
    db = get_database(allow_mutation=True)
    
    # Price mapping based on level
    price_mapping = {
        'Beginner': 499,
        'Intermediate': 999,
        'Advanced': 1499,
        'All Levels': 799
    }
    
    courses = db.courses.find()
    updated_count = 0
    
    print("🔄 Updating course prices to INR...\n")
    
    for course in courses:
        level = course.get('level', 'All Levels')
        new_price = price_mapping.get(level, 799)
        
        # Update the course
        db.courses.update_one(
            {'_id': course['_id']},
            {'$set': {'price': new_price}}
        )
        
        print(f"✅ {course.get('title')}")
        print(f"   Level: {level}")
        print(f"   Price: ₹{new_price}\n")
        updated_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Total courses updated: {updated_count}")
    print(f"   Average price: ₹{sum(price_mapping.values()) / len(price_mapping):.0f}")
    print(f"\n💰 Price Structure:")
    print(f"   Beginner: ₹499")
    print(f"   Intermediate: ₹999")
    print(f"   Advanced: ₹1,499")
    print(f"   All Levels: ₹799")
    
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
