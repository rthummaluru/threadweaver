import logging
from config import config
import anthropic
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=config.anthropic_api_key)

class LLMChatService:
    """
    LLM chat service class
    """
    def __init__(self):
        """
        Initialize the LLM chat service
        """
        self.client = client

    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Chat with the model
        """

        messages = [{"role": message.type.value, "content": message.content} for message in request.messages]

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages
            )
            return ChatResponse(response_message=ChatMessage(type=MessageType.ASSISTANT, content=response.content[0].text), query_used=f"Question: {request.messages[0].content}")
        except Exception as e:
            logger.error(f"Error chatting with the model: {e}")
            raise e