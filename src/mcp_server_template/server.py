"""
MCP Server Template

This module demonstrates all the key components of an MCP server:
- Tools: Functions that can be called by the LLM
- Prompts: Pre-defined prompt templates
- Resources: Data that can be accessed by the LLM
- Instructions: Server-level instructions for LLM behavior
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("mcp-server-template")


# ===== TOOLS =====
# Tools are functions that the LLM can call to perform actions


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="hello",
            description="Returns a friendly greeting message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet",
                    }
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="add",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
                },
                "required": ["a", "b"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "hello":
        person_name = arguments.get("name", "World")
        return [
            TextContent(
                type="text",
                text=f"Hello, {person_name}! 👋 Welcome to the MCP Server Template.",
            )
        ]
    elif name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [
            TextContent(
                type="text",
                text=f"The sum of {a} and {b} is {result}",
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


# ===== PROMPTS =====
# Prompts are pre-defined templates that can be used by the LLM


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List all available prompts."""
    return [
        Prompt(
            name="greeting",
            description="A friendly greeting prompt",
            arguments=[
                PromptArgument(
                    name="style",
                    description="The greeting style (formal or casual)",
                    required=False,
                )
            ],
        ),
        Prompt(
            name="code_review",
            description="A prompt template for code review",
            arguments=[
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=True,
                )
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific prompt."""
    if name == "greeting":
        style = arguments.get("style", "casual") if arguments else "casual"
        if style == "formal":
            message = "Good day! How may I assist you today?"
        else:
            message = "Hey there! What can I help you with?"

        return GetPromptResult(
            description=f"A {style} greeting",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=message),
                )
            ],
        )
    elif name == "code_review":
        language = arguments.get("language", "Python") if arguments else "Python"
        return GetPromptResult(
            description=f"Code review prompt for {language}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please review this {language} code for:\n"
                        f"1. Correctness and bugs\n"
                        f"2. Best practices\n"
                        f"3. Security issues\n"
                        f"4. Performance considerations\n"
                        f"5. Code style and readability",
                    ),
                )
            ],
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


# ===== RESOURCES =====
# Resources are data sources that the LLM can access


@server.list_resources()
async def list_resources() -> list[dict[str, str]]:
    """List all available resources."""
    return [
        {
            "uri": "template://info",
            "name": "Template Information",
            "description": "Information about this MCP server template",
            "mimeType": "text/plain",
        },
        {
            "uri": "template://examples",
            "name": "Example Code",
            "description": "Example code snippets",
            "mimeType": "text/plain",
        },
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "template://info":
        return """MCP Server Template

This is a template repository for creating MCP servers. It includes:
- Tools: Functions the LLM can call
- Prompts: Pre-defined prompt templates
- Resources: Data sources for the LLM
- Instructions: Server-level behavior guidance

Use this as a starting point for your own MCP server!
"""
    elif uri == "template://examples":
        return """Example MCP Tool Usage:

# Using the hello tool
result = await call_tool("hello", {"name": "Alice"})

# Using the add tool
result = await call_tool("add", {"a": 5, "b": 3})

# Using prompts
greeting = await get_prompt("greeting", {"style": "formal"})
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")


# ===== INSTRUCTIONS =====
# Server instructions guide the LLM on how to use this server


async def get_instructions() -> str:
    """Return server-level instructions for the LLM."""
    return """This MCP server provides example tools and resources.

When using this server:
1. Use the 'hello' tool to greet users by name
2. Use the 'add' tool to perform simple addition
3. Access template resources for information and examples
4. Use prompts for common interaction patterns

This is a template - customize it for your specific use case!
"""


# ===== MAIN =====


async def main() -> None:
    """Run the MCP server."""
    logger.info("Starting MCP Server Template")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def run() -> None:
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
