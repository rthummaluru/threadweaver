from fastapi import APIRouter
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType
from app.db.supabase_client import get_supabase_connection
from config import config

router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the model
    """
    test_message = ChatMessage(type=MessageType.ASSISTANT, content=f"I am answering the question: {request.messages[0].content}")

    return ChatResponse(response_message=test_message, query_used=f"Question: {request.messages[0].content}")