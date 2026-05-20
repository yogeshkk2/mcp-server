# MCP Server - Calculator Tools

A containerized **Model Context Protocol (MCP)** server built with Python and FastMCP. This server provides practical utility tools for temperature conversion and percentage calculations through an HTTP-based interface.

**Author:** Yogesh Kadiya

## Overview

This MCP server exposes multiple utility tools for common calculations and news fetching:

### Available Tools

1. **Celsius to Fahrenheit Converter**
   - **Function:** `convert_celsius_to_fahrenheit(celsius: float) -> str`
   - **Description:** Converts temperature values from Celsius to Fahrenheit scale
   - **Input:** Temperature in degrees Celsius
   - **Output:** Formatted string with both Celsius and Fahrenheit values (2 decimal places)
   - **Example:** `120°C is equal to 248.00°F`
   - **Error Handling:** Catches and reports conversion errors

2. **Percentage Calculator**
   - **Function:** `calculate_percentage(part: float, total: float) -> str`
   - **Description:** Calculates what percentage a given part represents of the total
   - **Inputs:**
     - `part`: The portion or subset value
     - `total`: The whole or 100% value
   - **Output:** Formatted string showing the percentage (2 decimal places)
   - **Example:** `25 is 50.00% of 50`
   - **Error Handling:** Prevents division by zero errors

3. **Latest News Fetcher**
   - **Function:** `get_latest_news(query: str = "technology", language: str = "en", max_results: int = 5) -> str`
   - **Description:** Fetches the latest news articles based on a search query from NewsAPI
   - **Inputs:**
     - `query`: Search topic (e.g., "technology", "sports", "business", "python programming")
     - `language`: ISO 639-1 language code (default: "en" for English)
     - `max_results`: Maximum number of articles to return, 1-100 (default: 5)
   - **Output:** Formatted string containing article titles, descriptions, sources, publication dates, and URLs
   - **Example:** Returns top 5 articles about Python programming in English
   - **Error Handling:** Handles network timeouts, connection errors, and API errors gracefully

4. **Top Headlines Fetcher**
   - **Function:** `get_top_headlines(country: str = "us", category: str = "general", max_results: int = 5) -> str`
   - **Description:** Fetches top headlines for a specific country and category from NewsAPI
   - **Inputs:**
     - `country`: ISO 2-letter country code (e.g., "us", "uk", "in", "fr", "de", "ca")
     - `category`: News category - business, entertainment, general, health, science, sports, technology
     - `max_results`: Maximum number of articles to return, 1-100 (default: 5)
   - **Output:** Formatted string containing headline articles with details
   - **Example:** Returns top 5 technology headlines from the United States
   - **Error Handling:** Validates inputs and handles API errors

### Additional Features

- **Dynamic Greeting Resource:** `greeting://{name}` - Provides personalized greetings
- **Prompt Generation:** Create greeting prompts in different styles (friendly, formal, casual)

### News API Integration

The news fetching tools use **NewsAPI.org** (free tier) to provide real-time news data:

- **API Endpoint:** https://newsapi.org/v2/
- **Free Tier:** 100 requests per day
- **Setup:**
  1. Sign up for a free account at https://newsapi.org/
  2. Go to the **API Keys** section in your NewsAPI dashboard.
  3. Create a new API key if you don't already have one, or generate a replacement key when required.
  4. Set the environment variable for your runtime environment:
     - macOS/Linux: `export NEWSAPI_KEY="your_api_key"`
     - Windows PowerShell: `$env:NEWSAPI_KEY = "your_api_key"`
     - Docker: use `-e NEWSAPI_KEY=your_api_key` when running the container
  5. If no API key is set, the tools will use the default demo key with limited functionality.

**Example Usage:**
```python
# Get latest technology news
get_latest_news("artificial intelligence", language="en", max_results=10)

# Get top headlines from the UK in sports category
get_top_headlines(country="uk", category="sports", max_results=5)
```

## Project Structure

```
mcp-server/
├── server.py                    # Main FastMCP server with tool definitions
├── tools/
│   ├── __init__.py
│   ├── calculator.py            # Calculator tool implementations
│   └── server.py                # Flask application with socket handling
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── justfile                     # Local task runner commands
└── README.md                    # This file
```

## Technologies Used

- **FastMCP:** FastAPI-based Model Context Protocol server framework
- **Flask:** Lightweight web framework for HTTP endpoints
- **Python 3.11:** Programming language and runtime
- **Docker:** Containerization for deployment
- **uvicorn:** ASGI server for HTTP transport
- **Just:** Simple task runner for project commands

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- pip or uv package manager

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yogeskk2/mcp-server.git
   cd mcp-server
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables** (Optional)
   ```bash
   export MCP_HOST=0.0.0.0
   export MCP_PORT=8000
   ```

### Running the Server

#### Option 1: Direct Python Execution
```bash
python server.py
```

The server will start on `http://localhost:8000` with streamable HTTP transport.

#### Option 2: Docker Container

1. **Build the Docker Image**
   ```bash
   docker build -t mcp-server .
   ```

2. **Run the Container**
   ```bash
   docker run -p 8000:8000 \
     -e MCP_HOST=0.0.0.0 \
     -e MCP_PORT=8000 \
     mcp-server
   ```

   The server will be accessible at `http://localhost:8000`

## Usage

### Calling Tools

Once the server is running, you can invoke the tools via MCP client:

#### Example 1: Temperature Conversion
```json
{
  "tool": "convert_celsius_to_fahrenheit",
  "arguments": {
    "celsius": 0
  }
}
```
**Response:** `"0°C is equal to 32.00°F"`

#### Example 2: Percentage Calculation
```json
{
  "tool": "calculate_percentage",
  "arguments": {
    "part": 25,
    "total": 100
  }
}
```
**Response:** `"25 is 25.00% of 100"`

### Server Endpoints

- **Status Check:** `GET /status`
  - Response: `{"status": "MCP server is running"}`
- **Main MCP Handler:** `http://localhost:8000` (POST requests via streamable HTTP transport)

## Configuration

Configuration settings are defined in [tools/server.py](tools/server.py):

```python
HOST = '0.0.0.0'           # Server listening address
PORT = 5000                # Flask server port
DEBUG = True               # Debug mode
```

### Environment Variables

- `MCP_HOST`: MCP server hostname (default: `0.0.0.0`)
- `MCP_PORT`: MCP server port (default: `8000`)

## API Documentation

### MCP Tools

| Tool | Parameters | Returns | Purpose |
|------|-----------|---------|---------|
| `convert_celsius_to_fahrenheit` | `celsius: float` | `str` | Convert Celsius to Fahrenheit |
| `calculate_percentage` | `part: float, total: float` | `str` | Calculate percentage of part relative to total |

### Resources

| Resource | Parameters | Purpose |
|----------|-----------|---------|
| `greeting://{name}` | `name: str` | Generate personalized greeting |

### Prompts

| Prompt | Parameters | Purpose |
|--------|-----------|---------|
| `greet_user` | `name: str, style: str` | Create styled greeting prompts |

## Error Handling

Both calculation tools include robust error handling:

- **Temperature Converter:** Catches and reports conversion exceptions
- **Percentage Calculator:** Validates that total is not zero before calculation

## Development

### Project Layout

- **Main Server:** [server.py](server.py) - FastMCP server initialization and tool definitions
- **Flask App:** [tools/server.py](tools/server.py) - Secondary HTTP server with socket handling
- **Calculator Tools:** [tools/calculator.py](tools/calculator.py) - Calculator tool implementations

### Adding New Tools

To add new tools to the MCP server, edit [server.py](server.py) and use the `@mcp.tool()` decorator:

```python
@mcp.tool()
def your_tool(param1: str, param2: int) -> str:
    """Tool description"""
    # Implementation
    return result
```

## Dependencies

See [requirements.txt](requirements.txt) for a complete list. Key dependencies:

- `mcp==1.27.1` - Model Context Protocol library
- `Flask` - Web framework
- `uvicorn` - ASGI server
- `requests` - HTTP client library
- `numpy` - Numerical computing
- `pandas` - Data manipulation
- `flask-socketio` - WebSocket support

## Deployment

### Docker Deployment

The project includes a `Dockerfile` for containerization. The image:
- Uses Python 3.11-slim as base
- Installs dependencies from `requirements.txt`
- Exposes port 8000
- Runs the MCP server on startup

### Running Tests

To verify the server is working:

```bash
# After starting the server, in another terminal:
curl http://localhost:5000/status
```

Expected response:
```json
{
  "status": "MCP server is running"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change `MCP_PORT` environment variable or stop the service using the port |
| Dependencies missing | Run `pip install -r requirements.txt` |
| Docker build fails | Ensure Docker is running and `python:3.11-slim` image is available |
| Connection refused | Verify server is running and check `MCP_HOST` and `MCP_PORT` settings |

## Future Enhancements

- Add additional utility tools (unit conversions, calculations)
- Implement caching for frequently used calculations
- Add logging and monitoring capabilities
- Create a web dashboard for tool testing
- Add comprehensive unit tests

## License

This project is provided as-is for educational and commercial use.

## Author

**Yogesh Kadiya**

## Support

For issues, questions, or suggestions, please refer to the project documentation or contact the author.

## Dependencies

The required Python dependencies are listed in `requirements.txt`. Make sure to install them if you are running the server outside of Docker.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. 

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
