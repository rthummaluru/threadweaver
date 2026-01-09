from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType, SessionCreateResponse, MessageListResponse
from app.db.supabase_client import get_supabase_connection
from config import config
from app.services.llm_chat_service import LLMChatService
from app.auth.dependencies import get_current_user_id
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["sessions"])


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, current_user_id: str = Depends(get_current_user_id)) -> MessageListResponse:
    """
    Get all messages in a session
    """
    try:
        logger.info(f"Getting messages for session: {session_id}")
        supabase_client = get_supabase_connection()

        # Check if the session exists and belongs to the current user
        session = supabase_client.table("chat_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user_id)\
            .single()\
            .execute()

        if not session.data:
            raise HTTPException(status_code=404, detail="Session not found")

        response = supabase_client.table("messages").select("*").eq("session_id", session_id).order("created_at", desc=False).execute()
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
                logger.warning(f"Malformed message in database: {e}, Message data: {msg}")
                continue

        return MessageListResponse(messages=messages)

    except Exception as e:
        logger.error(f"Error getting messages for session: {e}")
        raise HTTPException(status_code=500, detail=f"Unable to get messages for session. Please try again later.")