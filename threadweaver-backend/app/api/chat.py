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
   
    try:
        response = await llm_chat_service.chat(request)
        logger.info(f"Response: {response}")

        # Insert the assistant message into the messages table
        insert_assistant_message(supabase_client, response)
        return response


    except Exception as e:
        logger.error(f"Error chatting with the model: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
    

def insert_user_message(supabase_client: Client, request: ChatRequest):
    """
    Insert the user message into the messages table
    """
    try:
        supabase_client.table("messages").insert({
            "session_id": request.session_id,
            "role": MessageType.USER,
            "content": request.messages[0].content,
        }).execute()
    except Exception as e:
        logger.error(f"Error inserting user message into the messages table: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def insert_assistant_message(supabase_client: Client, response: ChatResponse):
    """
    Insert the assistant message into the messages table
    """
    try:
        supabase_client.table("messages").insert({
            "session_id": response.session_id,
            "role": MessageType.ASSISTANT,
            "content": response.response_message.content,
        }).execute()
    except Exception as e:
        logger.error(f"Error inserting assistant message into the messages table: {e}")
        raise HTTPException(status_code=500, detail=str(e))