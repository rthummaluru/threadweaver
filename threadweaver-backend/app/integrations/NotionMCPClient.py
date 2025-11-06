import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

from config import config


server_params = StdioServerParameters(
    command="npx",
    args=["-y","@notionhq/notion-mcp-server"],
    env={"NOTION_TOKEN": config.notion_token},
)

@asynccontextmanager
async def connect_to_notion_mcp_server() -> AsyncIterator[ClientSession]:
    """
    Context manager for connecting to Notion MCP server.
    Usage:
        async with connect_to_notion_mcp_server() as session:
            # Use session here
            tools = await session.list_tools()
            ...
    """
    # Connect with the Notion MCP Server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initiate the MCP client session
            await session.initialize()
            yield session


async def main():
    """Example usage of the Notion MCP client"""
    async with connect_to_notion_mcp_server() as session:
        # List available tools from the MCP server
        tools = await session.list_tools()
        tool_names = [tool.name for tool in tools.tools] if hasattr(tools, 'tools') else []
        print(f"Available tools: {tool_names}")

        result = await session.call_tool("API-post-search", {"query": "when was the page created?"})
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())