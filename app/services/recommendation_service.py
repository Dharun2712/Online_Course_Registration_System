"""
Recommendation Service - AI-powered course recommendations using Groq LLM
"""
import requests
import os
from app.utils.logger import log_error, log_info

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

class RecommendationService:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.model = MODEL
        self.base_url = GROQ_API_BASE
    
    def recommend_courses(self, user_profile, available_courses=None):
        """
        Generate personalized course recommendations
        Args:
            user_profile: Dictionary with user info (interests, completed courses, goals)
            available_courses: List of available courses to consider
        Returns:
            List of recommended course titles or categories
        """
        if not self.api_key:
            log_error("Groq API key not configured", "recommendation_service")
            return []
        
        try:
            # Build recommendation prompt
            prompt = self._build_recommendation_prompt(user_profile, available_courses)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert educational advisor specializing in personalized course recommendations. Provide specific, actionable course suggestions based on user profiles."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 800,
                "top_p": 1
            }
            
            log_info("Generating course recommendations...")
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations_text = data['choices'][0]['message']['content']
                log_info("Recommendations generated successfully")
                return self._parse_recommendations(recommendations_text)
            else:
                log_error(f"Groq API error: {response.status_code}", "recommendation_service")
                return []
        
        except Exception as e:
            log_error(str(e), "recommendation_service")
            return []
    
    def _build_recommendation_prompt(self, user_profile, available_courses=None):
        """Build prompt for course recommendations"""
        prompt = "Based on the following user profile, recommend 5 online courses:\n\n"
        
        # Add user profile information
        if user_profile.get('interests'):
            prompt += f"Interests: {', '.join(user_profile['interests'])}\n"
        
        if user_profile.get('completed_courses'):
            prompt += f"Completed Courses: {', '.join(user_profile['completed_courses'])}\n"
        
        if user_profile.get('career_goals'):
            prompt += f"Career Goals: {user_profile['career_goals']}\n"
        
        if user_profile.get('skill_level'):
            prompt += f"Current Skill Level: {user_profile['skill_level']}\n"
        
        # Add available courses if provided
        if available_courses:
            prompt += "\nAvailable Courses:\n"
            for course in available_courses[:20]:  # Limit to avoid token limits
                prompt += f"- {course.get('title', '')}: {course.get('description', '')[:100]}...\n"
            prompt += "\nRecommend from the above courses, or suggest similar course topics.\n"
        
        prompt += "\nProvide recommendations in this format:\n1. Course Title - Brief reason why\n2. Course Title - Brief reason why\n..."
        
        return prompt
    
    def _parse_recommendations(self, text):
        """Parse recommendations from AI response"""
        recommendations = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for numbered recommendations
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                recommendation = line.lstrip('0123456789.-) ').strip()
                if recommendation:
                    recommendations.append(recommendation)
        
        return recommendations[:5]  # Return top 5
    
    def get_learning_path(self, goal, current_level="beginner"):
        """
        Generate a learning path to achieve a goal
        Args:
            goal: Learning goal (e.g., "become a web developer")
            current_level: Current skill level
        Returns:
            Structured learning path
        """
        if not self.api_key:
            return {"error": "AI service not configured"}
        
        try:
            prompt = f"""Create a structured learning path for someone who wants to {goal}.
Current skill level: {current_level}

Provide a step-by-step learning path with:
1. Beginner courses (if applicable)
2. Intermediate courses
3. Advanced courses
4. Projects to build
5. Estimated timeline

Keep it practical and focused on online learning."""
            
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert career counselor and educational planner."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                learning_path = data['choices'][0]['message']['content']
                return {"success": True, "path": learning_path}
            else:
                return {"error": "Failed to generate learning path"}
        
        except Exception as e:
            log_error(str(e), "recommendation_service")
            return {"error": str(e)}
    
    def match_courses_to_skills(self, target_skills, available_courses):
        """
        Match courses to target skills
        Args:
            target_skills: List of skills user wants to learn
            available_courses: List of available courses
        Returns:
            Matched courses with relevance scores
        """
        # Simple matching based on tags and description
        matched = []
        
        for course in available_courses:
            score = 0
            course_text = f"{course.get('title', '')} {course.get('description', '')} {' '.join(course.get('tags', []))}".lower()
            
            for skill in target_skills:
                if skill.lower() in course_text:
                    score += 1
            
            if score > 0:
                matched.append({
                    "course": course,
                    "relevance_score": score
                })
        
        # Sort by relevance
        matched.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return matched[:10]  # Return top 10 matches
    
    def get_enrollment_based_recommendations(self, enrolled_courses, all_courses, count=5):
        """
        Get recommendations based on enrollment history
        Args:
            enrolled_courses: List of courses the student is enrolled in
            all_courses: List of all available courses
            count: Number of recommendations to return (default 5)
        Returns:
            List of recommended courses
        """
        if not enrolled_courses or not all_courses:
            # Return top rated or most popular courses as default
            return sorted(all_courses, key=lambda x: x.get('rating', 0), reverse=True)[:count]
        
        # Extract categories and tags from enrolled courses
        enrolled_categories = set()
        enrolled_tags = set()
        
        for course in enrolled_courses:
            if course.get('category'):
                enrolled_categories.add(course['category'].lower())
            if course.get('tags'):
                enrolled_tags.update([tag.lower() for tag in course['tags']])
        
        # Score each available course
        recommendations = []
        enrolled_ids = {str(course.get('_id', '')) for course in enrolled_courses}
        
        for course in all_courses:
            course_id = str(course.get('_id', ''))
            
            # Skip already enrolled courses
            if course_id in enrolled_ids:
                continue
            
            score = 0
            
            # Category match (higher weight)
            if course.get('category', '').lower() in enrolled_categories:
                score += 3
            
            # Tag matches
            if course.get('tags'):
                matching_tags = sum(1 for tag in course['tags'] if tag.lower() in enrolled_tags)
                score += matching_tags * 2
            
            # Level progression (suggest next level)
            if enrolled_courses:
                avg_level = sum(1 if c.get('level') == 'beginner' else 2 if c.get('level') == 'intermediate' else 3 for c in enrolled_courses) / len(enrolled_courses)
                course_level = 1 if course.get('level') == 'beginner' else 2 if course.get('level') == 'intermediate' else 3
                
                # Prefer courses slightly above current level
                if course_level == int(avg_level) + 1:
                    score += 2
                elif course_level == int(avg_level):
                    score += 1
            
            # Rating boost
            score += course.get('rating', 0) * 0.5
            
            if score > 0:
                recommendations.append({
                    'course': course,
                    'score': score
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [item['course'] for item in recommendations[:count]]

# Create singleton instance
recommendation_service = RecommendationService()

def get_recommendations(user_profile, available_courses=None):
    """Convenience function to get recommendations"""
    return recommendation_service.recommend_courses(user_profile, available_courses)

