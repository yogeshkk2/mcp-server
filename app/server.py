from flask import Flask, request, jsonify
import threading
import socket

app = Flask(__name__)

# Configuration settings
HOST = '0.0.0.0'
PORT = 5000

# Function to handle client connections
def handle_client_connection(client_socket):
    request_data = client_socket.recv(1024)
    print(f"Received: {request_data.decode('utf-8')}")
    response = "Message received"
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "MCP server is running"}), 200

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    app.run(host=HOST, port=PORT)