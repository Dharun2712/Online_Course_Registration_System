"""
Exam Model - Quiz and Exam Management
Supports 10-question quizzes with 1-5 marks per question
Pass mark: 5/total marks
"""
from datetime import datetime
from bson import ObjectId

class Exam:
    def __init__(self, db):
        self.collection = db['exams']
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for faster queries"""
        self.collection.create_index([('course_id', 1)])
        self.collection.create_index([('instructor_id', 1)])
        self.collection.create_index([('scheduled_at', 1)])
        self.collection.create_index([('status', 1)])
    
    def create_exam(self, exam_data):
        """
        Create a new exam
        exam_data = {
            'course_id': ObjectId,
            'instructor_id': ObjectId,
            'title': str,
            'description': str,
            'questions': [
                {
                    'question': str,
                    'options': ['A', 'B', 'C', 'D'],
                    'correct_answer': 'A',
                    'marks': 1-5,
                    'explanation': str (optional)
                }
            ],  # Must have exactly 10 questions
            'total_marks': int (sum of all question marks),
            'pass_marks': 5,
            'duration_minutes': int,
            'scheduled_at': datetime,
            'status': 'draft|scheduled|completed'
        }
        """
        exam = {
            'course_id': exam_data['course_id'],
            'instructor_id': exam_data['instructor_id'],
            'title': exam_data['title'],
            'description': exam_data.get('description', ''),
            'questions': exam_data['questions'],  # Exactly 10 questions
            'total_marks': exam_data['total_marks'],
            'pass_marks': 5,  # Fixed passing criteria
            'duration_minutes': exam_data.get('duration_minutes', 60),
            'scheduled_at': exam_data.get('scheduled_at'),
            'status': exam_data.get('status', 'draft'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(exam)
        exam['_id'] = result.inserted_id
        return self._serialize(exam)
    
    def get_exam(self, exam_id):
        """Get exam by ID"""
        exam = self.collection.find_one({'_id': ObjectId(exam_id)})
        return self._serialize(exam) if exam else None
    
    def get_course_exams(self, course_id):
        """Get all exams for a course"""
        exams = list(self.collection.find({'course_id': ObjectId(course_id)}))
        return [self._serialize(exam) for exam in exams]
    
    def get_instructor_exams(self, instructor_id):
        """Get all exams created by instructor"""
        exams = list(self.collection.find({'instructor_id': ObjectId(instructor_id)}))
        return [self._serialize(exam) for exam in exams]
    
    def update_exam(self, exam_id, updates):
        """Update exam details"""
        updates['updated_at'] = datetime.utcnow()
        self.collection.update_one(
            {'_id': ObjectId(exam_id)},
            {'$set': updates}
        )
        return self.get_exam(exam_id)
    
    def delete_exam(self, exam_id):
        """Delete exam"""
        result = self.collection.delete_one({'_id': ObjectId(exam_id)})
        return result.deleted_count > 0
    
    def _serialize(self, exam):
        """Convert ObjectId to string"""
        if exam:
            exam['_id'] = str(exam['_id'])
            exam['course_id'] = str(exam['course_id'])
            exam['instructor_id'] = str(exam['instructor_id'])
        return exam


class ExamSubmission:
    """Track student exam submissions and grades"""
    def __init__(self, db):
        self.collection = db['exam_submissions']
        self._create_indexes()
    
    def _create_indexes(self):
        self.collection.create_index([('exam_id', 1), ('student_id', 1)], unique=True)
        self.collection.create_index([('student_id', 1)])
        self.collection.create_index([('course_id', 1)])
    
    def submit_exam(self, submission_data):
        """
        Submit student answers
        submission_data = {
            'exam_id': ObjectId,
            'student_id': ObjectId,
            'course_id': ObjectId,
            'answers': [
                {'question_index': 0, 'selected_answer': 'A'}
            ],
            'score': int,
            'total_marks': int,
            'passed': bool,
            'time_taken_minutes': int
        }
        """
        submission = {
            'exam_id': submission_data['exam_id'],
            'student_id': submission_data['student_id'],
            'course_id': submission_data['course_id'],
            'answers': submission_data['answers'],
            'score': submission_data['score'],
            'total_marks': submission_data['total_marks'],
            'passed': submission_data['score'] >= 5,  # Pass if score >= 5
            'time_taken_minutes': submission_data.get('time_taken_minutes'),
            'submitted_at': datetime.utcnow()
        }
        
        result = self.collection.insert_one(submission)
        submission['_id'] = result.inserted_id
        return self._serialize(submission)
    
    def get_submission(self, exam_id, student_id):
        """Get student's exam submission"""
        submission = self.collection.find_one({
            'exam_id': ObjectId(exam_id),
            'student_id': ObjectId(student_id)
        })
        return self._serialize(submission) if submission else None
    
    def get_student_submissions(self, student_id):
        """Get all exam submissions by student"""
        submissions = list(self.collection.find({'student_id': ObjectId(student_id)}))
        return [self._serialize(sub) for sub in submissions]
    
    def get_exam_submissions(self, exam_id):
        """Get all submissions for an exam"""
        submissions = list(self.collection.find({'exam_id': ObjectId(exam_id)}))
        return [self._serialize(sub) for sub in submissions]
    
    def _serialize(self, submission):
        if submission:
            submission['_id'] = str(submission['_id'])
            submission['exam_id'] = str(submission['exam_id'])
            submission['student_id'] = str(submission['student_id'])
            submission['course_id'] = str(submission['course_id'])
        return submission
