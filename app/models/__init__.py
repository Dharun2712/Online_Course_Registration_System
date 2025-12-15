"""
Model package initialization
Makes models easily importable
"""
from app.models.user_model import User
from app.models.course_model import Course
from app.models.enrollment_model import Enrollment
from app.models.progress_model import Progress
from app.models.payment_model import Payment

__all__ = [
    'User',
    'Course',
    'Enrollment',
    'Progress',
    'Payment'
]
