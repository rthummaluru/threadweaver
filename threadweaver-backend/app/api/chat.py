from fastapi import APIRouter, HTTPException
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType
from app.db.supabase_client import get_supabase_connection
from config import config
from app.services.llm_chat_service import LLMChatService
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the model
    """
    llm_chat_service = LLMChatService()
   
    try:
        response = llm_chat_service.chat(request)
        logger.info(f"Chat response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error chatting with the model: {e}")
        raise HTTPException(status_code=500, detail=str(e))