import os
import socket
import threading

# Get the port from the environment variable PORT or default to 443
PORT = int(os.environ.get('PORT', 443))
HOST = '0.0.0.0'  # Listen on all network interfaces

# Function to handle client connections
def handle_client(client, username):
    print(f"[NEW CONNECTION] {username} connected.")

    connected = True
    while connected:
        # Receive message from client
        msg = client.recv(1024).decode('utf-8')
        if msg == "quit":
            connected = False
        else:
            print(f"[{username}] {msg}")
            broadcast(username, msg)

    client.close()

# Function to broadcast message to all clients except the sender
def broadcast(username, msg):
    for client, _ in clients:
        try:
            client.send(f"[{username}] {msg}".encode('utf-8'))
        except BrokenPipeError:
            # Handle the broken pipe error (client disconnected)
            print(f"Client disconnected unexpectedly.")

# List to store connected clients
clients = []

# Initialize server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[LISTENING] Server is listening on port {PORT}")

# Accept incoming connections and start a new thread for each client
while True:
    client_socket, _ = server.accept()
    username = client_socket.recv(1024).decode('utf-8')
    clients.append((client_socket, username))
    thread = threading.Thread(target=handle_client, args=(client_socket, username))
    thread.start()
