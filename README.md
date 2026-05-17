# MCP Server

This project is a containerized MCP (Multi-Channel Protocol) server built using Python. It includes various tools for managing and inspecting MCP connections.

## Project Structure

```
mcp-server
├── app
│   ├── __init__.py
│   ├── server.py
│   ├── tools
│   │   ├── __init__.py
│   │   └── inspector.py
│   └── config.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

To get started with the MCP server, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/mcp-server.git
   cd mcp-server
   ```

2. **Build the Docker Image**
   ```bash
   docker build -t mcp-server .
   ```

3. **Run the Docker Container**
   ```bash
   docker run -p 8000:8000 mcp-server
   ```

   This command will run the MCP server and expose it on port 8000.

## Usage

Once the server is running, you can connect to it using the MCP inspector tool. The inspector allows you to interact with the server and inspect the MCP tools.

## Configuration

Configuration settings for the server and tools can be found in `app/config.py`. Modify this file to adjust connection parameters and other constants as needed.

## Dependencies

The required Python dependencies are listed in `requirements.txt`. Make sure to install them if you are running the server outside of Docker.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. 

## License

This project is licensed under the MIT License. See the LICENSE file for more details.