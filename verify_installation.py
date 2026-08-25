"""
Installation Verification Script
Run this to check if everything is set up correctly
"""
import sys
import os

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    required_packages = [
        'flask',
        'flask_cors',
        'pymongo',
        'dotenv',
        'jwt',
        'werkzeug',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'jwt':
                __import__('jwt')
            else:
                __import__(package.replace('_', '-'))
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing.append(package)
    
    return len(missing) == 0

def check_environment_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file - Found")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['MONGO_URI', 'GROQ_API_KEY', 'SECRET_KEY']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} - Set")
        else:
            print(f"❌ {var} - Not set")
            missing.append(var)
    
    return len(missing) == 0

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        'app',
        'app/models',
        'app/routes',
        'app/services',
        'app/utils',
        'templates',
        'static',
        'static/js',
        'scripts'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ - Found")
        else:
            print(f"❌ {directory}/ - Missing")
            all_exist = False
    
    return all_exist

def check_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from dotenv import load_dotenv
        from db_connection import get_database
        load_dotenv()
        
        mongo_uri = os.getenv('MONGO_URI') or os.getenv('CUSTOMCONNSTR_MONGO_URI')
        if not mongo_uri:
            print("❌ MongoDB - MONGO_URI not set in .env")
            return False
        
        database = get_database()
        database.client.server_info()
        print("✅ MongoDB - Connection successful")
        client.close()
        return True
    except Exception as e:
        print(f"❌ MongoDB - Connection failed: {e}")
        return False

def check_groq_api():
    """Test Groq API key"""
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ Groq API - API key not set in .env")
            return False
        
        # Simple test (just check if key format is valid)
        if len(api_key) > 20:
            print("✅ Groq API - API key configured")
            return True
        else:
            print("⚠️  Groq API - API key seems invalid")
            return False
    except Exception as e:
        print(f"⚠️  Groq API - Could not verify: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("  CourseHub Platform - Installation Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    print("📋 Checking Python Version...")
    if not check_python_version():
        all_checks_passed = False
    print()
    
    print("📦 Checking Dependencies...")
    if not check_dependencies():
        all_checks_passed = False
        print("\n💡 Run: pip install -r requirements.txt")
    print()
    
    print("⚙️  Checking Environment Configuration...")
    if not check_environment_file():
        all_checks_passed = False
    print()
    
    print("📁 Checking Directory Structure...")
    if not check_directory_structure():
        all_checks_passed = False
    print()
    
    print("🔌 Testing MongoDB Connection...")
    if not check_mongodb_connection():
        all_checks_passed = False
    print()
    
    print("🤖 Checking Groq API Configuration...")
    check_groq_api()  # Don't fail on this
    print()
    
    print("=" * 60)
    if all_checks_passed:
        print("✅ All checks passed! You're ready to run the application.")
        print()
        print("Next steps:")
        print("1. python scripts/db_init.py  - Initialize database")
        print("2. python run.py              - Start the application")
        print("3. Visit http://localhost:3000")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
