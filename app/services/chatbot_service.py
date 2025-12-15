"""
Chatbot Service - AI-powered chatbot using Groq LLM API (Llama 3.3-70B)
Provides conversational assistance for course queries
"""
import requests
import os
from app.utils.logger import log_error, log_info

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

class ChatbotService:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = MODEL
        self.base_url = GROQ_API_BASE
    
    def get_response(self, user_message, context=None, conversation_history=None):
        """
        Get AI response from Groq API
        Args:
            user_message: User's question/message
            context: Additional context (course info, user profile, etc.)
            conversation_history: List of previous messages for context
        Returns:
            AI response text or error message
        """
        if not self.api_key:
            log_error("Groq API key not configured", "chatbot_service")
            return "Sorry, the AI service is not configured properly."
        
        try:
            # Build system prompt
            system_prompt = self._build_system_prompt(context)
            
            # Build messages array
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 1,
                "stream": False
            }
            
            log_info(f"Chatbot request: {user_message[:50]}...")
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_message = data['choices'][0]['message']['content']
                log_info("Chatbot response generated successfully")
                return ai_message
            else:
                log_error(f"Groq API error: {response.status_code} - {response.text}", "chatbot_service")
                return "Sorry, I'm having trouble processing your request. Please try again."
        
        except requests.exceptions.Timeout:
            log_error("Groq API timeout", "chatbot_service")
            return "Sorry, the request timed out. Please try again."
        
        except Exception as e:
            log_error(str(e), "chatbot_service")
            return "Sorry, an error occurred while processing your request."
    
    def _build_system_prompt(self, context=None):
        """Build system prompt with context"""
        base_prompt = """You are an intelligent course assistant for CourseHub, an online learning platform. 
Your role is to help students find courses, answer questions about learning, provide study tips, 
and assist with platform navigation.

Be helpful, friendly, and concise. When discussing courses:
- Recommend courses based on user interests
- Explain course benefits and learning outcomes
- Provide information about instructors, pricing, and duration
- Help with enrollment questions

If you don't have specific information, politely say so and guide users to contact support."""
        
        if context:
            base_prompt += f"\n\nCurrent Context:\n{context}"
        
        return base_prompt
    
    def ask_about_course(self, course_info, user_question):
        """
        Answer questions about a specific course
        Args:
            course_info: Dictionary with course details
            user_question: User's question about the course
        """
        context = f"""
Course Information:
- Title: {course_info.get('title', 'N/A')}
- Description: {course_info.get('description', 'N/A')}
- Price: ${course_info.get('price', 0)}
- Level: {course_info.get('level', 'N/A')}
- Duration: {course_info.get('duration', 'N/A')}
- Tags: {', '.join(course_info.get('tags', []))}
"""
        
        return self.get_response(user_question, context)
    
    def get_study_tips(self, subject=None):
        """Get study tips for a subject"""
        if subject:
            message = f"Give me effective study tips for learning {subject}. Keep it concise and actionable."
        else:
            message = "Give me general study tips for online learning. Keep it concise and actionable."
        
        return self.get_response(message)
    
    def explain_concept(self, concept, level="beginner"):
        """Explain a learning concept"""
        message = f"Explain {concept} in simple terms for a {level} level learner. Use examples if helpful."
        return self.get_response(message)
    
    def career_guidance(self, field):
        """Provide career guidance"""
        message = f"What career paths are available in {field}? What skills should someone learn to succeed in this field?"
        return self.get_response(message)

# Create singleton instance
chatbot_service = ChatbotService()

def chat_response(message, context=None):
    """Convenience function to get chat response"""
    return chatbot_service.get_response(message, context)
