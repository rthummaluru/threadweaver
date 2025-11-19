from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict, List
from enum import Enum
import uuid 
from datetime import datetime


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
    created_at: datetime = Field(default=datetime.now(), description="The date and time the message was created")

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

class SessionCreateRequest(BaseModel):
    """
    Session create request schema
    """
    title: Optional[str] = Field(default='New Session', description="Optional title of the session")

class SessionCreateResponse(BaseModel):
    """
    Session create response schema
    """
    session_id: uuid.UUID = Field(..., description="The id of the session")
    title: Optional[str] = Field(..., description="Optional title of the session")
    created_at: datetime = Field(..., description="The date and time the session was created")
    updated_at: datetime = Field(..., description="The date and time the session was updated")

class MessageListResponse(BaseModel):
    """
    Message list response schema
    """
    messages: List[ChatMessage] = Field(..., description="The messages in the session")