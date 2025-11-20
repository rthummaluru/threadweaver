from fastapi import APIRouter, HTTPException
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType, SessionCreateResponse, MessageListResponse
from app.db.supabase_client import get_supabase_connection
from config import config
from app.services.llm_chat_service import LLMChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["sessions"])


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str) -> MessageListResponse:
    """
    Get all messages in a session
    """
    try:
        logger.info(f"Getting messages for session: {session_id}")
        supabase_client = get_supabase_connection()

        response = supabase_client.table("messages").select("*").eq("session_id", session_id).order("created_at", asc=True).execute()
        logger.info(f" Messages Database Response: {response}")

        messages = []
        for msg in response.data:
            try:
                chat_message = ChatMessage(
                    type=msg["role"],
                    content=msg["content"]
                )
                messages.append(chat_message)
            except KeyError as e:
                logger.error(f"Missing field in message: {e}")
                # Skip malformed messages or raise

        return MessageListResponse(messages=messages)

    except Exception as e:
        logger.error(f"Error getting messages for session: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting messages for session: {e}")