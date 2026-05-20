"""
MCP Server - Calculator and News Tools

A Model Context Protocol (MCP) server providing utility tools for calculations and news fetching.

Author: Yogesh Kadiya
Description: This server exposes tools for temperature conversion (Celsius to Fahrenheit),
             percentage calculations, and real-time news fetching through an HTTP-based
             MCP interface using NewsAPI for news data.

Features:
    - Celsius to Fahrenheit temperature conversion
    - Percentage calculation utility
    - Latest news fetching by search query
    - Top headlines fetching by country and category
    - Dynamic greeting resources
    - Customizable greeting prompts

Run the server:
    python server.py

The server will start on the configured MCP_HOST and MCP_PORT (default: localhost:8000)
with streamable HTTP transport.

Environment Variables:
    MCP_HOST: Server host (default: 0.0.0.0)
    MCP_PORT: Server port (default: 8000)
    NEWSAPI_KEY: Your NewsAPI.org API key (optional, default: demo key with limited requests)
"""

import os
from mcp.server.fastmcp import FastMCP
from tools import calculator, news

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


@mcp.tool()
def get_latest_news(
    query: str = "technology",
    language: str = "en",
    max_results: int = 5
) -> str:
    """
    Fetch the latest news articles based on a search query.
    
    Args:
        query: Search topic (e.g., 'technology', 'sports', 'business')
        language: ISO 639-1 language code (e.g., 'en', 'es', 'fr')
        max_results: Maximum number of articles to return (1-100, default: 5)
    
    Returns:
        Formatted string containing latest news articles with titles and descriptions.
    """
    return news.get_latest_news(query, language=language, max_results=max_results)


@mcp.tool()
def get_top_headlines(
    country: str = "us",
    category: str = "general",
    max_results: int = 5
) -> str:
    """
    Fetch top headlines for a specific country and category.
    
    Args:
        country: ISO 2-letter country code (e.g., 'us', 'uk', 'in', 'fr', 'de')
        category: News category - business, entertainment, general, health, science, sports, technology
        max_results: Maximum number of articles to return (1-100, default: 5)
    
    Returns:
        Formatted string containing top headline articles with titles and descriptions.
    """
    return news.get_top_headlines(country, category=category if category != "general" else None, max_results=max_results)


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
    print("  - get_latest_news")
    print("  - get_top_headlines")
    print("\nAvailable resources:")
    print("  - greeting://{name}")
    print("\nAvailable prompts:")
    print("  - greet_user")
    print("\nServer running on streamable HTTP transport...")
    mcp.run(transport="streamable-http")