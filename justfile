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
	python3 -m pip install -r requirements.txt

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
