FROM python:3.11-slim

# Set the working directory
WORKDIR /mcp-server

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . .

# Expose the MCP server port
EXPOSE 8000

# Default host/port for the MCP server
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

# Neo4j configuration
# NEO4J_URI: Neo4j bolt URI for the service
# NEO4J_USER: Neo4j username
# NEO4J_PASSWORD: Neo4j password; the app defaults to Kyndryl@123 when unset
ENV NEO4J_URI=bolt://neo4j:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=Kyndryl@123

# Optional API keys and service credentials
ENV NEWSAPI_KEY=2c8b34b19ace4152bb605d364d1d3426

# Command to run the server
CMD ["python", "server.py"]