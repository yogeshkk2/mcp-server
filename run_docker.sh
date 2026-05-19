#!/usr/bin/env bash

set -euo pipefail

IMAGE_NAME="mcp-server"
CONTAINER_NAME="mcp-server-container"
PORT="8000"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed or not on PATH." >&2
  exit 1
fi

echo "Building Docker image '$IMAGE_NAME' from Dockerfile..."
docker build -t "$IMAGE_NAME" .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing existing container '${CONTAINER_NAME}'..."
  docker rm -f "$CONTAINER_NAME"
fi

echo "Running Docker container '$CONTAINER_NAME' on host port $PORT..."
docker run -d --name "$CONTAINER_NAME" -p "$PORT":8000 "$IMAGE_NAME"

echo "Container started. MCP server should be available on http://localhost:$PORT"
echo "You can test it with the MCP inspector by connecting to port $PORT."
