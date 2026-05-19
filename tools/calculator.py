"""Calculator tools for the MCP server."""


def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """Convert Celsius to Fahrenheit and format the result."""
    try:
        fahrenheit = (celsius * 9 / 5) + 32
        return f"{celsius}°C is equal to {fahrenheit:.2f}°F"
    except Exception as e:
        return f"Error during conversion: {str(e)}"


def calculate_percentage(part: float, total: float) -> str:
    """Calculate the percentage that part represents of total."""
    if total == 0:
        return "Error: Division by zero. Total cannot be zero."

    percentage = (part / total) * 100
    return f"{part} is {percentage:.2f}% of {total}"
