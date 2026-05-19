"""Flask application server module for the MCP project."""

from flask import Flask, request, jsonify
import threading
import socket

# Initialize Flask application
app = Flask(__name__)

# Configuration settings
HOST = '0.0.0.0'
PORT = 5000


def handle_client_connection(client_socket):
    """Handle individual client connections on the socket server."""
    try:
        request_data = client_socket.recv(1024)
        print(f"Received: {request_data.decode('utf-8')}")
        response = "Message received"
        client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    """Start a multi-threaded TCP socket server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_socket,),
                daemon=True
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()


@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint that returns the server status."""
    return jsonify({"status": "MCP server is running"}), 200


if __name__ == '__main__':
    socket_thread = threading.Thread(target=start_server, daemon=True)
    socket_thread.start()
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
