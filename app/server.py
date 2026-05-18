"""
Flask Application Server Module

This module implements a secondary HTTP server for the MCP Server project.
It provides Flask endpoints and socket-based client handling capabilities.

Author: Yogesh Kadiya

Features:
    - Flask-based HTTP server for REST endpoints
    - Multi-threaded socket server for TCP client handling
    - Health check endpoint for server status monitoring
    - Concurrent client connection handling
"""

from flask import Flask, request, jsonify
import threading
import socket

# Initialize Flask application
app = Flask(__name__)

# Configuration settings
HOST = '0.0.0.0'
PORT = 5000


def handle_client_connection(client_socket):
    """
    Handle individual client connections on the socket server.
    
    This function processes incoming messages from clients and sends responses.
    It runs in a separate thread for each connected client.
    
    Args:
        client_socket (socket.socket): The connected client socket.
    
    Process:
        1. Receives data from client (max 1024 bytes)
        2. Logs received message
        3. Sends acknowledgment message
        4. Closes the connection
    """
    try:
        # Receive data from client (blocking, max 1024 bytes)
        request_data = client_socket.recv(1024)
        print(f"Received: {request_data.decode('utf-8')}")
        
        # Prepare response message
        response = "Message received"
        
        # Send response back to client
        client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Always close the socket when done
        client_socket.close()


def start_server():
    """
    Start a multi-threaded TCP socket server.
    
    This function:
    - Creates a server socket on HOST:PORT
    - Listens for incoming client connections
    - Spawns a new thread for each client connection
    - Continues accepting connections until interrupted
    
    The server runs indefinitely, accepting up to 5 pending connections
    in the queue before rejecting new connection attempts.
    """
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind socket to the host and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections (queue up to 5 pending connections)
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        # Continuously accept and handle client connections
        while True:
            # Accept a client connection (blocks until connection arrives)
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            
            # Create a new thread to handle this client
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_socket,),
                daemon=True  # Thread will terminate when main thread exits
            )
            
            # Start the handler thread
            client_handler.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


# ============================================================================
# FLASK ENDPOINTS
# ============================================================================

@app.route('/status', methods=['GET'])
def status():
    """
    Health check endpoint that returns the server status.
    
    Returns:
        dict: JSON response with server status information
        int: HTTP status code (200 = OK)
    
    Example Response:
        {"status": "MCP server is running"}
    """
    return jsonify({"status": "MCP server is running"}), 200


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == '__main__':
    # Start the socket server in a separate daemon thread
    # This allows the Flask server to run on the main thread
    socket_thread = threading.Thread(target=start_server, daemon=True)
    socket_thread.start()
    
    # Start Flask development server on the main thread
    # host='0.0.0.0' makes server accessible from any network interface
    # port=PORT specifies the listening port
    # debug=True enables auto-reload on code changes
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)

