"""
AI Routes - Groq AI Integration for Course Assistant
"""
from flask import Blueprint, request, jsonify, current_app
from app.utils.jwt_helper import token_required, get_current_user
import os
import requests

ai_bp = Blueprint('ai', __name__)

# Groq API configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')  # Set this in your .env file
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

@ai_bp.route('/chat', methods=['POST'])
@token_required
def chat():
    """
    AI chatbot endpoint using Groq AI
    Request body:
    {
        "message": "User's question",
        "course_id": "course_id",
        "context": "course_learning"
    }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        course_id = data.get('course_id')
        current_user = get_current_user()
        
        if not user_message:
            return jsonify({'success': False, 'message': 'Message is required'}), 400
        
        # Get course context if course_id is provided and DB is available
        course_context = ""
        if course_id:
            db = getattr(current_app, 'db', None)
            if db is not None:
                try:
                    from bson import ObjectId
                    # Handle both ObjectId and string formats
                    if isinstance(course_id, str) and len(course_id) == 24:
                        course_id = ObjectId(course_id)
                    course = db.courses.find_one({'_id': course_id})
                    if course:
                        course_context = f"Course: {course.get('title', '')}\nDescription: {course.get('description', '')}\n"
                except Exception as e:
                    # Ignore course context errors (fallback to no context)
                    print(f"Course context error: {e}")
                    course_context = ""
        
        # Check if Groq API key is configured
        if not GROQ_API_KEY:
            # Fallback response when API key is not configured
            return jsonify({
                'success': True,
                'response': f"I'm your course assistant! To enable AI-powered responses, please configure the GROQ_API_KEY environment variable.\n\nYour question: {user_message}\n\nFor now, here are some helpful tips:\n- Review the course materials in the Materials tab\n- Check the Live Sessions schedule\n- Practice with the course exercises\n- Reach out to your instructor for specific questions"
            }), 200
        
        # Prepare the prompt for Groq AI
        system_prompt = f"""You are an expert Computer Science and Programming tutor. You specialize in:
- Programming languages (Python, JavaScript, Java, C++, C#, etc.)
- Data structures and algorithms
- Software engineering principles
- Web development (frontend and backend)
- Database systems and SQL
- Object-oriented programming
- System design and architecture
- Debugging and problem-solving

{course_context}

CRITICAL FORMATTING RULES:
1. ALWAYS use bullet points (•) for each point - put each on a NEW LINE
2. Use **bold** for key terms and important concepts
3. Keep responses under 200 words
4. Put blank lines between sections for readability
5. End EVERY response with "Related Questions:" followed by 2 suggested follow-up questions

Required Format Structure:
[One sentence summary]

• **Key point 1** - brief explanation
• **Key point 2** - brief explanation  
• **Key point 3** - brief explanation

[Optional code example if needed - keep it 2-3 lines]

Related Questions:
• [Suggested question 1 based on current topic]
• [Suggested question 2 to explore deeper]

Example Response:
"Recursion is when a function calls itself to solve smaller instances of a problem.

• **Base Case** - the stopping condition that prevents infinite recursion
• **Recursive Case** - where function calls itself with modified parameters
• **Stack Overflow** - occurs when recursion goes too deep without base case

Related Questions:
• What's the difference between recursion and iteration?
• How do I optimize recursive functions?"

Always follow this format exactly."""
        
        # Call Groq AI API
        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'llama-3.1-8b-instant',  # Fast, efficient, and free model
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_message}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 512  # Reduced for more concise responses
                },
                timeout=12
            )

            # If non-200, log details and return a helpful fallback response
            if response.status_code != 200:
                try:
                    resp_text = response.text
                except Exception:
                    resp_text = '<unreadable response>'
                print(f"Groq API returned status {response.status_code}: {resp_text}")

                # Provide a useful offline fallback that still helps the student
                fallback = (
                    "I can't reach the AI service right now, but here are a few suggestions:\n"
                    "1) Re-check the course materials and module where this topic appears.\n"
                    "2) Look at related lectures or the recommended readings.\n"
                    "3) Try asking a more focused question (one concept at a time).\n"
                    "4) If it's urgent, contact your instructor with details.\n\n"
                    f"(Debug: Groq API status {response.status_code})"
                )

                return jsonify({'success': True, 'response': fallback}), 200

            groq_data = response.json()
            # Be defensive when parsing
            ai_response = ''
            try:
                ai_response = groq_data.get('choices', [])[0].get('message', {}).get('content', '')
            except Exception:
                ai_response = groq_data.get('choices', [])[0]['message']['content'] if groq_data.get('choices') else ''

            if not ai_response:
                ai_response = "I got a blank response from the AI service. Try rephrasing your question."

            return jsonify({'success': True, 'response': ai_response}), 200

        except requests.exceptions.Timeout:
            return jsonify({'success': True, 'response': "The AI request timed out. Try asking a shorter question or try again in a moment."}), 200
        except Exception as api_error:
            # Log the exception for debugging and return a helpful fallback
            print(f"Groq API Error: {api_error}")
            return jsonify({'success': True, 'response': "I encountered an error contacting the AI service. Try again later or contact your instructor."}), 200
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
