import logging
import time as t
from config import config
import anthropic
from app.schemas.requests import ChatRequest, ChatResponse, ChatMessage, MessageType, SearchResponse
from app.integrations.NotionMCPClient import connect_to_notion_mcp_server
from app.prompts.chat_system_prompt import system_prompt
from app.services.rag_service import RAGService

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
        self.rag_service = RAGService()

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
            logger.info(f"=============== Calling tool: {tool_name} ===============")
            result = await session.call_tool(tool_name, arguments)
            logger.info(f"=============== Tool result: {result} ===============")
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
    
    def _enhance_message_with_rag_context(self, user_query: str, rag_results: SearchResponse) -> str:
        """
        Enhance the last message with RAG context
        """
        rag_results_string = "\n\n".join([f"Document ID: {result.document_id} \n\n Chunk text: {result.chunk_text}" for result in rag_results.results])
        return f"<question>\n{user_query}\n</question> \n\n <context>\n{rag_results_string}\n</context>"

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
        
        logger.info("=============== Begin LLM workflow ===============")
        # Convert request messages to Anthropic format
        messages = [{"role": message.type.value, "content": message.content} for message in request.messages]

        # Step 0: Search the database for documents
        user_query = messages[-1]["content"]
        rag_results = self.rag_service.search(query=user_query, match_threshold=0.25, top_k=3)

        # Check if there are any relevant results from the RAG search
        if rag_results.results:
            # Add the RAG results as extra context to the last message
            context_enhanced_message = self._enhance_message_with_rag_context(user_query, rag_results)
            messages[-1]["content"] = context_enhanced_message
        else:
            logger.info(f"No relevant results found from the RAG search for user query: {user_query}")

        # Step 1: Get tools from MCP server (MCP Tool objects)
        tools = await self._get_notion_tools()
        
        # Step 2: Convert MCP tools to Anthropic format
        anthropic_tools = await self._get_anthropic_tools(tools)
        
        #logger.info(f"=== LLMChatService.chat: Tools converted to Anthropic format: {anthropic_tools} ===")
        
        try:
            # Step 3: First call to Claude with tools
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                tools=anthropic_tools,  # Pass tools to Claude
            )
            
           # logger.info(f"=== LLMChatService.chat: Response stop reason: {response.stop_reason} ===")
           # logger.info(f"=== LLMChatService.chat: Response content: {response.content} ===")

            # Step 4: Handle tool use loop
            current_messages = messages  # Track conversation history
            logger.info(f"=============== Current messages: {current_messages} ===============")
            
            # Keep looping as long as Claude wants to use tools
            start_time = t.time()
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
                    system=system_prompt,
                    messages=current_messages,  # Include conversation + tool result
                    tools=anthropic_tools,
                )

                end_time = t.time()
                logger.info(f"=============== Time taken to process tool use: {end_time - start_time} seconds ===============")

                start_time = end_time

            # Step 8: Return final response (when Claude is done using tools)
            return ChatResponse(
                session_id=request.session_id,
                response_message=ChatMessage(
                    type=MessageType.ASSISTANT, 
                    content=response.content[0].text
                ), 
                query_used=f"Question: {request.messages[0].content}"
            )
        except Exception as e:
            logger.error(f"Error chatting with the model: {e}")
            raise e