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

# Configuration from environment variables
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

# Create MCP server instance
# json_response=True ensures responses are properly formatted as JSON
mcp = FastMCP("Calculator Server", json_response=True, host=MCP_HOST, port=MCP_PORT)


@mcp.tool()
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """
    Converts a temperature value from Celsius to Fahrenheit scale.

    This tool performs temperature conversion using the standard formula:
    F = (C × 9/5) + 32

    Args:
        celsius (float): The temperature value in degrees Celsius to convert.

    Returns:
        str: A formatted string displaying both Celsius and Fahrenheit values
             with 2 decimal precision, or an error message if conversion fails.

    Examples:
        >>> convert_celsius_to_fahrenheit(0)
        '0°C is equal to 32.00°F'
        
        >>> convert_celsius_to_fahrenheit(100)
        '100°C is equal to 212.00°F'
        
        >>> convert_celsius_to_fahrenheit(-40)
        '-40°C is equal to -40.00°F'

    Raises:
        Catches all exceptions and returns an error message string.
    """
    try:
        # Apply the Celsius to Fahrenheit conversion formula
        fahrenheit = (celsius * 9/5) + 32

        # Format result to 2 decimal places for readability
        return f"{celsius}°C is equal to {fahrenheit:.2f}°F"
    except Exception as e:
        # Return error message if conversion fails
        return f"Error during conversion: {str(e)}"


@mcp.tool()
def calculate_percentage(part: float, total: float) -> str:
    """
    Calculates what percentage a given part represents of the total value.

    This tool uses the standard percentage formula:
    Percentage = (Part / Total) × 100

    Args:
        part (float): The portion or subset value to calculate percentage for.
        total (float): The whole or 100% reference value. Cannot be zero.

    Returns:
        str: A formatted string showing the part, percentage, and total values
             with 2 decimal precision, or an error message if calculation fails.

    Examples:
        >>> calculate_percentage(25, 100)
        '25 is 25.00% of 100'
        
        >>> calculate_percentage(1, 2)
        '1 is 50.00% of 2'
        
        >>> calculate_percentage(3, 4)
        '3 is 75.00% of 4'

    Raises:
        Returns error message if total is zero (division by zero).
        Catches all exceptions and returns an error message string.
    """
    # Check for division by zero
    if total == 0:
        return "Error: Division by zero. Total cannot be zero."

    # Calculate percentage using the standard formula
    # P = (part / total) * 100
    percentage = (part / total) * 100

    # Return formatted result with 2 decimal places
    return f"{part} is {percentage:.2f}% of {total}"


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