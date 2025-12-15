"""
Exam Service
Handles exam creation, scheduling, taking, and grading
"""
from datetime import datetime
from bson import ObjectId
import random

class ExamService:
    def __init__(self, db):
        self.db = db
        self.exam_collection = db['exams']
        self.submission_collection = db['exam_submissions']
        self.course_collection = db['courses']
        
    def create_exam(self, course_id, instructor_id, exam_data):
        """Create a new exam with flexible questions"""
        try:
            # Validate questions
            questions = exam_data.get('questions', [])
            if len(questions) < 1:
                return False, 'Exam must have at least 1 question'
            
            if len(questions) > 50:
                return False, 'Exam cannot have more than 50 questions'
            
            total_marks = 0
            for i, q in enumerate(questions):
                marks = q.get('marks', 1)
                if marks < 1 or marks > 100:
                    return False, f'Question {i+1}: Marks must be between 1 and 100'
                total_marks += marks
                
                # Validate question structure
                if not q.get('question'):
                    return False, f'Question {i+1}: Question text is required'
                if not q.get('options') or len(q.get('options')) < 2:
                    return False, f'Question {i+1}: At least 2 options are required'
                if q.get('correct_answer') is None:
                    return False, f'Question {i+1}: Correct answer must be specified'
            
            # Calculate passing marks from percentage
            passing_score_percent = exam_data.get('passing_score', 70)
            passing_marks = (total_marks * passing_score_percent) / 100
            
            # Parse dates
            exam_date = exam_data.get('exam_date')
            deadline = exam_data.get('deadline')
            
            exam_doc = {
                'course_id': ObjectId(course_id),
                'instructor_id': ObjectId(instructor_id),
                'title': exam_data.get('title'),
                'description': exam_data.get('description', ''),
                'questions': questions,
                'total_marks': total_marks,
                'passing_marks': round(passing_marks, 2),
                'passing_score_percent': passing_score_percent,
                'duration_minutes': exam_data.get('duration', exam_data.get('duration_minutes', 60)),
                'status': 'active',
                'is_published': True,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Add date fields if provided
            if exam_date:
                if isinstance(exam_date, str):
                    # Handle datetime-local format (YYYY-MM-DDTHH:MM)
                    try:
                        exam_doc['exam_date'] = datetime.strptime(exam_date, '%Y-%m-%dT%H:%M')
                    except ValueError:
                        exam_doc['exam_date'] = datetime.fromisoformat(exam_date.replace('Z', '+00:00'))
                else:
                    exam_doc['exam_date'] = exam_date
            if deadline:
                if isinstance(deadline, str):
                    # Handle datetime-local format (YYYY-MM-DDTHH:MM)
                    try:
                        exam_doc['deadline'] = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
                    except ValueError:
                        exam_doc['deadline'] = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                else:
                    exam_doc['deadline'] = deadline
            
            result = self.exam_collection.insert_one(exam_doc)
            
            return True, str(result.inserted_id)
            
        except Exception as e:
            return False, f'Error creating exam: {str(e)}'
    
    def get_exam(self, exam_id):
        """Get exam details"""
        try:
            exam = self.exam_collection.find_one({'_id': ObjectId(exam_id)})
            
            if not exam:
                return False, None
            
            exam['_id'] = str(exam['_id'])
            exam['course_id'] = str(exam['course_id'])
            exam['instructor_id'] = str(exam['instructor_id'])
            
            # Convert datetime fields if they exist
            if 'exam_date' in exam and exam['exam_date']:
                exam['exam_date'] = exam['exam_date'].isoformat()
            if 'scheduled_at' in exam and exam['scheduled_at']:
                exam['scheduled_at'] = exam['scheduled_at'].isoformat()
            if 'deadline' in exam and exam['deadline']:
                exam['deadline'] = exam['deadline'].isoformat()
            if 'created_at' in exam and exam['created_at']:
                exam['created_at'] = exam['created_at'].isoformat()
            if 'updated_at' in exam and exam['updated_at']:
                exam['updated_at'] = exam['updated_at'].isoformat()
            
            return True, exam
            
        except Exception as e:
            print(f"Error in get_exam: {str(e)}")
            return False, None
    
    def get_course_exams(self, course_id, include_questions=False):
        """Get all exams for a course"""
        try:
            exams = list(self.exam_collection.find({
                'course_id': ObjectId(course_id)
            }).sort('created_at', -1))
            
            for exam in exams:
                exam['_id'] = str(exam['_id'])
                exam['course_id'] = str(exam['course_id'])
                exam['instructor_id'] = str(exam['instructor_id'])
                
                # Convert datetime fields if they exist
                if 'exam_date' in exam and exam['exam_date']:
                    exam['exam_date'] = exam['exam_date'].isoformat()
                if 'deadline' in exam and exam['deadline']:
                    exam['deadline'] = exam['deadline'].isoformat()
                if 'scheduled_at' in exam and exam['scheduled_at']:
                    exam['scheduled_at'] = exam['scheduled_at'].isoformat()
                if 'created_at' in exam and exam['created_at']:
                    exam['created_at'] = exam['created_at'].isoformat()
                if 'updated_at' in exam and exam['updated_at']:
                    exam['updated_at'] = exam['updated_at'].isoformat()
                
                if not include_questions:
                    exam.pop('questions', None)
            
            return True, exams
            
        except Exception as e:
            print(f"Error in get_course_exams: {str(e)}")
            return False, []
    
    def submit_exam(self, exam_id, student_id, answers):
        """Submit exam answers"""
        try:
            # Get exam
            exam = self.exam_collection.find_one({'_id': ObjectId(exam_id)})
            if not exam:
                print(f"[ExamService] submit_exam: exam not found (exam_id={exam_id})")
                return False, 'Exam not found'
            
            # Check if already submitted
            existing = self.submission_collection.find_one({
                'exam_id': ObjectId(exam_id),
                'student_id': ObjectId(student_id)
            })
            
            if existing:
                print(f"[ExamService] submit_exam: exam already submitted (exam_id={exam_id}, student_id={student_id})")
                return False, 'Exam already submitted'
            
            # Calculate marks
            total_obtained = 0
            graded_answers = []
            
            for i, question in enumerate(exam['questions']):
                student_answer = answers.get(str(i))
                correct_answer = question.get('correct_answer')
                marks = question.get('marks', 0)
                
                # Convert both to int for comparison
                is_correct = False
                if student_answer is not None and correct_answer is not None:
                    try:
                        is_correct = int(student_answer) == int(correct_answer)
                    except (ValueError, TypeError):
                        is_correct = str(student_answer) == str(correct_answer)
                
                obtained = marks if is_correct else 0
                
                graded_answers.append({
                    'question_index': i,
                    'question_text': question.get('question', ''),
                    'student_answer': student_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'marks_obtained': obtained,
                    'max_marks': marks
                })
                
                total_obtained += obtained
            
            # Determine pass/fail
            passed = total_obtained >= exam['passing_marks']
            print(f"[ExamService] submit_exam: student={student_id} obtained={total_obtained}/{exam.get('total_marks')} passed={passed}")
            
            submission_doc = {
                'exam_id': ObjectId(exam_id),
                'student_id': ObjectId(student_id),
                'course_id': exam['course_id'],
                'exam_title': exam.get('title', 'Exam'),
                'answers': graded_answers,
                'total_marks': exam['total_marks'],
                'marks_obtained': total_obtained,
                'passing_marks': exam['passing_marks'],
                'passed': passed,
                'submitted_at': datetime.now(),
                'graded': True,
                'certificate_generated': False
            }
            
            result = self.submission_collection.insert_one(submission_doc)
            print(f"[ExamService] submit_exam: inserted submission_id={result.inserted_id}")
            
            return True, {
                'submission_id': str(result.inserted_id),
                'marks_obtained': total_obtained,
                'total_marks': exam['total_marks'],
                'passed': passed
            }
            
        except Exception as e:
            return False, f'Error submitting exam: {str(e)}'
    
    def grade_subjective_answers(self, submission_id, graded_answers):
        """Grade subjective answers manually (instructor)"""
        try:
            submission = self.submission_collection.find_one({'_id': ObjectId(submission_id)})
            if not submission:
                return False, 'Submission not found'
            
            # Update marks
            total_obtained = 0
            for graded in graded_answers:
                idx = graded['question_index']
                marks = graded['marks_obtained']
                
                # Find and update the answer
                for answer in submission['answers']:
                    if answer['question_index'] == idx:
                        answer['marks_obtained'] = marks
                        break
                
                total_obtained += marks
            
            # Calculate total including already graded questions
            for answer in submission['answers']:
                if answer['question_index'] not in [g['question_index'] for g in graded_answers]:
                    total_obtained += answer['marks_obtained']
            
            passed = total_obtained >= submission['passing_marks']
            
            self.submission_collection.update_one(
                {'_id': ObjectId(submission_id)},
                {
                    '$set': {
                        'answers': submission['answers'],
                        'marks_obtained': total_obtained,
                        'passed': passed,
                        'graded': True,
                        'graded_at': datetime.now()
                    }
                }
            )
            
            return True, {
                'marks_obtained': total_obtained,
                'passed': passed
            }
            
        except Exception as e:
            return False, f'Error grading exam: {str(e)}'
    
    def get_student_submissions(self, student_id, course_id=None):
        """Get all exam submissions for a student"""
        try:
            query = {'student_id': ObjectId(student_id)}
            if course_id:
                query['course_id'] = ObjectId(course_id)
            
            submissions = list(self.submission_collection.find(query).sort('submitted_at', -1))
            
            for sub in submissions:
                sub['_id'] = str(sub['_id'])
                sub['exam_id'] = str(sub['exam_id'])
                sub['student_id'] = str(sub['student_id'])
                sub['course_id'] = str(sub['course_id'])
                sub['submitted_at'] = sub['submitted_at'].isoformat()
            
            return True, submissions
            
        except Exception as e:
            return False, []
    
    def get_exam_submissions(self, exam_id):
        """Get all submissions for an exam (for instructor)"""
        try:
            submissions = list(self.submission_collection.find({
                'exam_id': ObjectId(exam_id)
            }))
            
            # Get student details
            for sub in submissions:
                student = self.db['users'].find_one({'_id': sub['student_id']})
                sub['_id'] = str(sub['_id'])
                sub['exam_id'] = str(sub['exam_id'])
                sub['student_id'] = str(sub['student_id'])
                sub['course_id'] = str(sub['course_id'])
                sub['student_name'] = student['name'] if student else 'Unknown'
                sub['student_email'] = student['email'] if student else 'Unknown'
                sub['submitted_at'] = sub['submitted_at'].isoformat()
                
                # Check if certificate exists
                cert = self.db['certificates'].find_one({'submission_id': sub['_id'] if isinstance(sub['_id'], ObjectId) else ObjectId(sub['_id'])})
                sub['certificate_id'] = str(cert['_id']) if cert else None
            
            return True, submissions
            
        except Exception as e:
            return False, []
