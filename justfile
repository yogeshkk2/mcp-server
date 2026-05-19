set shell := ["bash", "-lc"]

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
	python -m pip install -r requirements.txt

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm --name $(CONTAINER) -p $(PORT):8000 -e MCP_HOST=0.0.0.0 -e MCP_PORT=8000 $(IMAGE)

run-detached:
	docker run -d --name $(CONTAINER) -p $(PORT):8000 -e MCP_HOST=0.0.0.0 -e MCP_PORT=8000 $(IMAGE)

stop:
	-docker stop $(CONTAINER)

remove:
	-docker rm -f $(CONTAINER)

restart:
	just stop
	just remove
	just build
	just run-detached

logs:
	docker logs -f $(CONTAINER)

test:
	python - <<-'EOF'
	import os, sys
	import urllib.request
	url = f"http://localhost:{os.getenv('PORT', '8000')}/status"
	try:
	    with urllib.request.urlopen(url, timeout=5) as resp:
	        body = resp.read().decode('utf-8')
	        if resp.status == 200:
	            print('OK:', body)
	            sys.exit(0)
	        print('FAIL: HTTP', resp.status)
	        sys.exit(1)
	except Exception as e:
	    print('FAIL:', e)
	EOF
    sys.exit(1)
PY
