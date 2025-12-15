# AI Chatbot Setup Guide (Groq AI)

## Overview
The course learning page includes an AI-powered chatbot using Groq AI to help students with course questions.

## Setup Instructions

### 1. Get Groq API Key
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### 2. Configure Environment Variable
Add the following to your `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Features
- **Real-time chat**: Students can ask questions about the course
- **Context-aware**: Chatbot has access to course information (title, description)
- **Fallback mode**: Works even without API key (provides helpful responses)
- **Fast responses**: Uses Groq's Mixtral-8x7b model for quick answers

### 4. API Endpoint
**POST** `/api/ai/chat`

**Headers:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What is this course about?",
  "course_id": "course_id_here",
  "context": "course_learning"
}
```

**Response:**
```json
{
  "success": true,
  "response": "This course covers..."
}
```

### 5. Customization
Edit `app/routes/ai_routes.py` to:
- Change the AI model (`mixtral-8x7b-32768` or others)
- Adjust temperature (creativity level)
- Modify system prompt for different responses
- Add more context (materials, transcripts, etc.)

### 6. Rate Limits
- Groq free tier: 14,400 requests/day
- For production: Consider upgrading to paid tier

## Troubleshooting

**Chatbot shows fallback responses:**
- Verify `GROQ_API_KEY` is set in `.env`
- Check the console for API errors
- Ensure the API key is valid

**Slow responses:**
- Check network connection
- Verify Groq API status
- Consider caching common questions

**Error messages:**
- Check browser console for errors
- Verify JWT token is valid
- Ensure student is enrolled in the course

## Alternative AI Providers
You can easily swap Groq with other providers:
- **OpenAI**: Change API URL to `https://api.openai.com/v1/chat/completions`
- **Anthropic**: Use Claude API
- **Cohere**: Use Cohere API

Just update the API_URL and model name in `ai_routes.py`.
