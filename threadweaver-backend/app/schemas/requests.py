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

class ChatRequest(BaseModel):
    """
    Chat request schema
    """
    session_id: str = Field(..., description="The session id")
    messages: List[ChatMessage] = Field(..., description="The messages to chat")
    
class ChatResponse(BaseModel):
    """
    Chat response schema
    """
    session_id: str = Field(..., description="The session id")
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
    session_id: str = Field(..., description="The id of the session")
    title: Optional[str] = Field(..., description="Optional title of the session")
    created_at: datetime = Field(..., description="The date and time the session was created")
    updated_at: datetime = Field(..., description="The date and time the session was updated")

class MessageListResponse(BaseModel):
    """
    Message list response schema
    """
    messages: List[ChatMessage] = Field(..., description="The messages in the session")

class DocumentUploadResponse(BaseModel):
    """
    Document upload response schema
    """
    message: str = Field(..., description="Success message")
    document_id: str = Field(..., description="The ID of the uploaded document")
    chunks_created: int = Field(..., description="Number of chunks created")

class SearchResult(BaseModel):
    """
    Search result schema
    """
    chunk_text: str = Field(..., description="The raw text of the chunk")
    chunk_index: int = Field(..., description="The index of the chunk")
    similarity_score: float = Field(..., description="The similarity score of the chunk")
    document_id: str = Field(..., description="The id of the document the chunk belongs to")

class SearchResponse(BaseModel):
    """
    Search response schema
    """
    results: List[SearchResult] = Field(..., description="The search results")