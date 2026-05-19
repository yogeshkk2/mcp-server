set shell := ["sh", "-c"]

IMAGE := "mcp-server"
CONTAINER := "mcp-server-container"
PORT := "8000"

help:
	@echo "Available tasks:"
	@echo "  just install          Install Python dependencies"
	@echo "  just build            Build the Docker image"
	@echo "  just run              Run the container in the foreground"
	@echo "  just run-detached     Run the container in detached mode"
	@echo "  just stop             Stop the running container"
	@echo "  just remove           Remove the container if it exists"
	@echo "  just restart          Rebuild and restart the container"
	@echo "  just logs             Tail logs from the running container"
	@echo "  just test             Verify server health on http://localhost:$(PORT)/status"

install:
	#!/bin/bash

	# Exit immediately if a command exits with a non-zero status
	set -e

	# Define variables
	VENV_DIR=".venv"
	REQUIREMENTS_FILE="requirements.txt"

	echo "=== Starting Python Environment Setup ==="

	# 1. Check if Python 3 is installed
	if ! command -v python3 &> /dev/null; then
		echo "Error: Python 3 is not installed. Please install it and try again."
		exit 1
	fi

	# 2. Create a virtual environment if it doesn't exist
	if [ ! -d "$VENV_DIR" ]; then
		echo "Creating virtual environment in $VENV_DIR..."
		python3 -m venv "$VENV_DIR"
	else
		echo "Virtual environment already exists."
	fi

	# 3. Activate the virtual environment
	echo "Activating virtual environment..."
	source "$VENV_DIR/bin/activate"

	# 4. Upgrade pip to the latest version
	echo "Upgrading pip..."
	pip install --upgrade pip

	# 5. Install Python packages
	if [ -f "$REQUIREMENTS_FILE" ]; then
		echo "Installing packages from $REQUIREMENTS_FILE..."
		pip install -r "$REQUIREMENTS_FILE"
	else
		echo "No $REQUIREMENTS_FILE found. Installing a few default packages..."
		# You can list individual packages here if you don't want to use a requirements.txt
		pip install requests numpy pandas
	fi

	echo "=== Setup Complete! ==="
	echo "To activate this environment in your current terminal, run: source $VENV_DIR/bin/activate"

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm --name $(CONTAINER) -p $(PORT):8000 -e MCP_HOST=0.0.0.0 -e MCP_PORT=8000 $(IMAGE)

run-detached:
	docker run -d --name $(CONTAINER) -p $(PORT):8000 -e MCP_HOST=0.0.0.0 -e MCP_PORT=8000 $(IMAGE)

stop:
	docker stop $(CONTAINER) || true

remove:
	docker rm -f $(CONTAINER) || true

restart:
	just stop
	just remove
	just build
	just run-detached

logs:
	docker logs -f $(CONTAINER)

test:
	curl -f http://localhost:$(PORT)/status || exit 1
