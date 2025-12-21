from fastapi import APIRouter, HTTPException
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType, MessageListResponse
from app.db.supabase_client import get_supabase_connection
from config import config
from app.services.llm_chat_service import LLMChatService
from supabase import Client
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["chat"])

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the model
    """
    supabase_client = get_supabase_connection()
    logger.info(f"Received request: {request}")
    
    # Insert the user message into the messages table
    insert_user_message(supabase_client, request)
    
    llm_chat_service = LLMChatService()
    
    # Possible failure points:
    # - LLM API call fails
    try:
        response = await llm_chat_service.chat(request)
        logger.info(f"Response: {response}")

        # Insert the assistant message into the messages table
        insert_assistant_message(supabase_client, response)
        return response
    # Re-raise HTTPExceptions handled by helper functions
    except HTTPException:
        raise
    # Handle client-side errors
    except (ValueError, IndexError, KeyError):
        logger.error(f"Client-side error: {e}")
        raise HTTPException(status_code=400, detail="Invalid request data")
    # Handle database errors
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=503, detail="A database error occurred while processing your request")

def insert_user_message(supabase_client: Client, request: ChatRequest):
    """
    Insert the user message into the messages table
    """
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="Request must contain at least one message.")
        
        supabase_client.table("messages").insert({
            "session_id": request.session_id,
            "role": MessageType.USER,
            "content": request.messages[-1].content,
        }).execute()

    except Exception as e:
        logger.error(f"Error inserting user message into the messages table: {e}")
        raise HTTPException(status_code=503, detail="Unable to save message. Please try again later.")

def insert_assistant_message(supabase_client: Client, response: ChatResponse):
    """
    Insert the assistant message into the messages table
    """
    try:
        if not response.response_message:
            raise HTTPException(status_code=400, detail="Response must contain a message.")
        
        supabase_client.table("messages").insert({
            "session_id": response.session_id,
            "role": MessageType.ASSISTANT,
            "content": response.response_message.content,
        }).execute()
    except Exception as e:
        logger.error(f"Error inserting assistant message into the messages table: {e}")
        raise HTTPException(status_code=503, detail="Unable to save message. Please try again later.")