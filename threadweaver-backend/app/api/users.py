from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType, SessionCreateResponse
from app.db.supabase_client import get_supabase_connection
from config import config
from app.services.llm_chat_service import LLMChatService
from app.auth.dependencies import get_current_user_id
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["users"])


@router.get("/users/sessions/current")
async def get_current_user_session(current_user_id: str = Depends(get_current_user_id)) -> SessionCreateResponse:
    """
    Returns the most recent session for a user
    """
    logger.info(f"Getting current session for user: {current_user_id}")
    supabase_client = get_supabase_connection()

    try:
        # Get the most recent session for the user
        logger.info(f"Getting most recent session for user: {current_user_id}")
        response = supabase_client.table("chat_sessions").select("*").eq("user_id", current_user_id).order("updated_at", desc=True).limit(1).execute()
        logger.info(f" Current Session Database Response: {response}")

        if response.data and len(response.data) > 0:
            return SessionCreateResponse(
                session_id=response.data[0]["id"],
                title=response.data[0]["title"],
                created_at=response.data[0]["created_at"],
                updated_at=response.data[0]["updated_at"],
            )
        else:
            # Create a new session for the user if not found
            logger.info(f"No session found for user: {current_user_id}, creating new session")
            supabase_client.table('chat_sessions').insert({
                "user_id": current_user_id,
                "title": 'New Session',
            }).execute()

            logger.info(f"New session created for user: {current_user_id}")
            response = supabase_client.table("chat_sessions").select("*").eq("user_id", current_user_id).order("created_at", desc=True).limit(1).execute()
            logger.info(f" New Session Database Response: {response}")
            
            return SessionCreateResponse(
                session_id=response.data[0]["id"],
                title=response.data[0]["title"],
                created_at=response.data[0]["created_at"],
                updated_at=response.data[0]["updated_at"],
            )

    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=503, detail=f"Unable to get current session for user. Please try again later.")
        
    