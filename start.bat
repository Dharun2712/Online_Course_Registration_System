@echo off
echo ==========================================
echo  CourseHub - Online Learning Platform
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Initialize database
echo Initializing database...
python scripts\db_init.py
echo.

REM Run the application
echo Starting Flask application...
echo.
echo ==========================================
echo  Application will be available at:
echo  http://localhost:5000
echo ==========================================
echo.
echo Sample Credentials:
echo.
echo Admin:      admin@coursehub.com / Admin@123
echo Instructor: sarah@coursehub.com / Instructor@123  
echo Student:    john@student.com / Student@123
echo.
echo ==========================================
echo.

python run.py

pause
