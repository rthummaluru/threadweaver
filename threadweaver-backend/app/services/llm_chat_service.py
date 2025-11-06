import logging
from config import config
import anthropic
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType
from app.integrations.NotionMCPClient import connect_to_notion_mcp_server

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

    async def _get_notion_tools(self):
        """
        Get available Notion tools from MCP server.
        Returns a list of tool names and their descriptions.
        """
        async with connect_to_notion_mcp_server() as session:
            tools = await session.list_tools()
            print(f"Test Tools: {[tool for tool in tools.tools] if hasattr(tools, 'tools') else []}")
            return tools.tools if hasattr(tools, 'tools') else []

    async def _call_notion_tool(self, tool_name: str, arguments: dict):
        """
        Call a Notion MCP tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        async with connect_to_notion_mcp_server() as session:
            result = await session.call_tool(tool_name, arguments)
            return result
    
    async def _convert_notion_tools_to_anthropic(self, tools: list):
        """
        Convert Notion tools to Anthropic tools.
        """
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })
        return anthropic_tools

    async def _get_anthropic_tools(self, tools: list):
        """
        Get Anthropic tools.
        """
        return await self._convert_notion_tools_to_anthropic(tools)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Chat with the model. Uses Notion MCP tools when available.
        """
        messages = [{"role": message.type.value, "content": message.content} for message in request.messages]
        tools = await self._get_notion_tools()
        anthropic_tools = await self._get_anthropic_tools(tools)
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages,
                tools=anthropic_tools,
            )
            return ChatResponse(response_message=ChatMessage(type=MessageType.ASSISTANT, content=response.content[0].text), query_used=f"Question: {request.messages[0].content}")
        except Exception as e:
            logger.error(f"Error chatting with the model: {e}")
            raise e