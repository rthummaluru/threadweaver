from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict, List
from enum import Enum

class MessageType(str, Enum):
    """
    Message type enum
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """
    Chat message schema
    """
    type: MessageType = Field(..., description="The type of the message")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    """
    Chat request schema
    """
    # TO BE IMPLEMENTED: session_id: str = Field(..., description="The session id")
    messages: List[ChatMessage] = Field(..., description="The messages to chat")

class ChatResponse(BaseModel):
    """
    Chat response schema
    """
    response_message: ChatMessage = Field(..., description="The message to chat")
    query_used: str = Field(..., description="The query used to generate the response")



