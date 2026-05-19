"""
MCP Server - Calculator Tools

A Model Context Protocol (MCP) server providing utility tools for common calculations.

Author: Yogesh Kadiya
Description: This server exposes tools for temperature conversion (Celsius to Fahrenheit)
             and percentage calculations through an HTTP-based MCP interface.

Features:
    - Celsius to Fahrenheit temperature conversion
    - Percentage calculation utility
    - Dynamic greeting resources
    - Customizable greeting prompts

Run the server:
    python server.py

The server will start on the configured MCP_HOST and MCP_PORT (default: localhost:8000)
with streamable HTTP transport.
"""

import os
from mcp.server.fastmcp import FastMCP
from tools import calculator

# Configuration from environment variables
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

# Create MCP server instance
# json_response=True ensures responses are properly formatted as JSON
mcp = FastMCP("Calculator Server", json_response=True, host=MCP_HOST, port=MCP_PORT)


@mcp.tool()
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """Forward the Celsius-to-Fahrenheit conversion to the calculator module."""
    return calculator.convert_celsius_to_fahrenheit(celsius)


@mcp.tool()
def calculate_percentage(part: float, total: float) -> str:
    """Forward percentage calculations to the calculator module."""
    return calculator.calculate_percentage(part, total)


# ============================================================================
# RESOURCES AND PROMPTS
# ============================================================================

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Generates a personalized greeting message for the given name.

    This resource provides a simple way to get customized greetings that can be
    used as context or starting points for other operations.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A friendly personalized greeting message.

    Examples:
        >>> get_greeting("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """
    Generates a greeting prompt with customizable style for creating greetings.

    This prompt can be used with language models to create styled greetings
    for different contexts and communication preferences.

    Args:
        name (str): The name of the person to greet.
        style (str): The style of greeting to generate. Options:
                    - "friendly": Warm, approachable greeting
                    - "formal": Professional, business-like greeting
                    - "casual": Relaxed, informal greeting
                    Defaults to "friendly" if invalid style is provided.

    Returns:
        str: A prompt string that instructs an LLM to generate a greeting.

    Examples:
        >>> greet_user("Bob", "formal")
        'Please write a formal, professional greeting for someone named Bob.'
        
        >>> greet_user("Charlie", "casual")
        'Please write a casual, relaxed greeting for someone named Charlie.'
    """
    # Define greeting style templates
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    # Get the appropriate style template, default to friendly if not found
    style_template = styles.get(style, styles['friendly'])

    # Return the complete prompt
    return f"{style_template} for someone named {name}."


# ============================================================================
# SERVER STARTUP
# ============================================================================

# Run the MCP server with streamable HTTP transport
# This allows for efficient streaming of responses over HTTP
if __name__ == "__main__":
    print(f"Starting MCP Server on {MCP_HOST}:{MCP_PORT}...")
    print("Available tools:")
    print("  - convert_celsius_to_fahrenheit")
    print("  - calculate_percentage")
    print("\nAvailable resources:")
    print("  - greeting://{name}")
    print("\nAvailable prompts:")
    print("  - greet_user")
    print("\nServer running on streamable HTTP transport...")
    mcp.run(transport="streamable-http")