# AI Chat Router - Claude 3.5 Sonnet Integration for Agent Reality Map
# Provides AI-powered chat interface with LaTeX/Markdown support

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from anthropic import Anthropic

router = APIRouter()

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

class ConversationMessage(BaseModel):
    role: str
    content: str
    timestamp: int

class ChatRequest(BaseModel):
    user_input: str
    context: Optional[Dict] = {}

class ChatResponse(BaseModel):
    response: str
    model: str = "claude-3-5-sonnet-20240620"

SYSTEM_PROMPT = """You are an AI assistant helping developers with software development tasks.

You have expertise in:
- Software architecture and design patterns
- Code optimization and best practices
- Debugging and problem-solving
- API development and integration
- Database design and queries
- Testing strategies
- DevOps and CI/CD
- Agent-based systems and swarm coordination
- Real-time WebSocket communication
- FastAPI and React development

Provide clear, concise, and practical advice. When relevant, include code examples.
You can use Markdown formatting and LaTeX math notation ($...$) in your responses.
"""

@router.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(request: ChatRequest):
    """
    AI chat endpoint using Claude 3.5 Sonnet

    Supports:
    - Markdown formatting
    - LaTeX math notation ($...$)
    - Code blocks with syntax highlighting
    - Conversation history context
    """
    try:
        # Build conversation context
        conversation_history = request.context.get("conversation_history", [])

        # Prepare messages for Anthropic
        messages = []
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current user input
        messages.append({
            "role": "user",
            "content": request.user_input
        })

        # Call Anthropic API
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        # Extract response text
        response_text = message.content[0].text

        return ChatResponse(
            response=response_text,
            model="claude-3-5-sonnet-20240620"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing AI request: {str(e)}"
        )
