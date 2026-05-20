FROM python:3.11-slim

# Set the working directory
WORKDIR /mcp-server

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the MCP server port
EXPOSE 8000

# Default host/port for the MCP server
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV NEWSAPI_KEY=2c8b34b19ace4152bb605d364d1d3426

# Command to run the server
CMD ["python", "server.py"]