#!/bin/bash

echo "=========================================="
echo " CourseHub - Online Learning Platform"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Initialize database
echo "Initializing database..."
python scripts/db_init.py
echo ""

# Run the application
echo "Starting Flask application..."
echo ""
echo "=========================================="
echo " Application will be available at:"
echo " http://localhost:5000"
echo "=========================================="
echo ""
echo "Sample Credentials:"
echo ""
echo "Admin:      admin@coursehub.com / Admin@123"
echo "Instructor: sarah@coursehub.com / Instructor@123"
echo "Student:    john@student.com / Student@123"
echo ""
echo "=========================================="
echo ""

python run.py
