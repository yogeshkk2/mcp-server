"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

import os
from mcp.server.fastmcp import FastMCP

MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

# Create an MCP server
mcp = FastMCP("Demo", json_response=True, host=MCP_HOST, port=MCP_PORT)


# Add an addition tool
#@mcp.tool()
#def add(a: int, b: int) -> int:
#    """Add two numbers"""
#    return a + b



@mcp.tool()
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """
    Converts a temperature from Celsius to Fahrenheit.

    Args:
        celsius: The temperature in degrees Celsius.
    """
    try:
        # Perform the conversion
        fahrenheit = (celsius * 9/5) + 32

        # Format to 2 decimal places for cleanliness
        return f"{celsius}°C is equal to {fahrenheit:.2f}°F"
    except Exception as e:
        return f"Error during conversion: {str(e)}"



@mcp.tool()
def calculate_percentage(part: float, total: float) -> str:
    """
    Calculates the percentage of a value relative to a total.

    Args:
        part: The portion or subset value.
        total: The whole or 100% value.
    """
    if total == 0:
        return "Error: Division by zero. Total cannot be zero."

    # Using the standard percentage formula:
    # P = (part / total) * 100
    percentage = (part / total) * 100

    return f"{part} is {percentage:.2f}% of {total}"

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")