install:
	python -m pip install -r requirements.txt

run:
	python server.py

docker-build:
	docker build -t mcp-server .

docker-run:
	docker run -p 8000:8000 -e MCP_HOST=0.0.0.0 -e MCP_PORT=8000 mcp-server
