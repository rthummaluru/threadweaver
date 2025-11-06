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
        
        Connects to the Notion MCP server and retrieves all available tools.
        Returns a list of MCP Tool objects (not yet in Anthropic format).
        
        Returns:
            list: List of MCP Tool objects with name, description, inputSchema, etc.
        """
        # Use context manager to ensure connection is properly closed
        async with connect_to_notion_mcp_server() as session:
            # Request list of available tools from MCP server
            tools = await session.list_tools()
            # Debug: Print tools to see what we're getting
            print(f"Test Tools: {[tool for tool in tools.tools] if hasattr(tools, 'tools') else []}")
            # Extract the tools list from the response (MCP returns a list in .tools attribute)
            return tools.tools if hasattr(tools, 'tools') else []

    async def _call_notion_tool(self, tool_name: str, arguments: dict):
        """
        Call a Notion MCP tool with the given arguments.
        
        This executes a tool on the Notion MCP server (e.g., search, retrieve page, etc.)
        Each call creates a new connection to the MCP server.
        
        Args:
            tool_name: Name of the MCP tool to call (e.g., "API-post-search")
            arguments: Dictionary of arguments required by the tool
            
        Returns:
            CallToolResult: Result object containing the tool's response
        """
        # Create a new MCP connection for this tool call
        async with connect_to_notion_mcp_server() as session:
            # Execute the tool on the MCP server
            result = await session.call_tool(tool_name, arguments)
            return result
    
    async def _convert_notion_tools_to_anthropic(self, tools: list):
        """
        Convert MCP Tool objects to Anthropic's tool format.
        
        MCP tools have: name, description, inputSchema (capital S)
        Anthropic expects: name, description, input_schema (lowercase s)
        
        Args:
            tools: List of MCP Tool objects
            
        Returns:
            list: List of dictionaries in Anthropic's tool format
        """
        anthropic_tools = []
        for tool in tools:
            # Convert each MCP tool to Anthropic format
            anthropic_tools.append({
                "name": tool.name,  # Tool name stays the same
                "description": tool.description,  # Description stays the same
                "input_schema": tool.inputSchema  # Note: inputSchema -> input_schema (lowercase)
            })
        return anthropic_tools

    async def _get_anthropic_tools(self, tools: list):
        """
        Convert MCP tools to Anthropic format.
        
        This is a convenience wrapper around the conversion function.
        
        Args:
            tools: List of MCP Tool objects
            
        Returns:
            list: List of tools in Anthropic format
        """
        return await self._convert_notion_tools_to_anthropic(tools)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Chat with Claude, with support for Notion MCP tools.
        
        This method:
        1. Gets Notion tools from MCP server
        2. Converts them to Anthropic format
        3. Sends them to Claude along with the user's message
        4. If Claude wants to use a tool, executes it and loops back with the result
        5. Returns Claude's final response
        
        Args:
            request: ChatRequest containing user messages
            
        Returns:
            ChatResponse with Claude's response
        """
        # Convert request messages to Anthropic format
        messages = [{"role": message.type.value, "content": message.content} for message in request.messages]
        
        # Step 1: Get tools from MCP server (MCP Tool objects)
        tools = await self._get_notion_tools()
        
        # Step 2: Convert MCP tools to Anthropic format
        anthropic_tools = await self._get_anthropic_tools(tools)
        
        try:
            # Step 3: First call to Claude with tools
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages,
                tools=anthropic_tools,  # Pass tools to Claude
            )
            
            # Debug: Check what Claude wants to do
            print(f"Response stop reason: {response.stop_reason}")
            print(f"Response content: {response.content}")

            # Step 4: Handle tool use loop
            current_messages = messages  # Track conversation history
            
            # Keep looping as long as Claude wants to use tools
            while response.stop_reason == "tool_use":
                # Find the tool_use block in Claude's response
                tool_blocks = [block for block in response.content if block.type == "tool_use"]
                
                tool_results = []
                if tool_blocks:
                    for tool_block in tool_blocks:
                    # Extract tool name and arguments from Claude's request
                        result = await self._call_notion_tool(tool_block.name, tool_block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_block.id,
                            "content": str(result.content)
                        })

                current_messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                current_messages.append({
                    "role": "user",
                    "content": tool_results
                })

                # Step 7: Send tool result back to Claude and get response
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    messages=current_messages,  # Include conversation + tool result
                    tools=anthropic_tools,
                )

            # Step 8: Return final response (when Claude is done using tools)
            return ChatResponse(
                response_message=ChatMessage(
                    type=MessageType.ASSISTANT, 
                    content=response.content[0].text
                ), 
                query_used=f"Question: {request.messages[0].content}"
            )
        except Exception as e:
            logger.error(f"Error chatting with the model: {e}")
            raise e