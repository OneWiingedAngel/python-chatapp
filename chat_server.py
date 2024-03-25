import os
import socket
import threading

PORT = int(os.environ.get('PORT', 443))
HOST = '0.0.0.0'

# Function to get the IP address of the server
def get_server_ip():
    return socket.gethostbyname(socket.gethostname())

def handle_client(client, username):
    print(f"[NEW CONNECTION] {username} connected.")

    connected = True
    while connected:
        msg = client.recv(1024).decode('utf-8')
        if msg == "quit":
            connected = False
        else:
            broadcast(username, msg)

    client.close()

def broadcast(sender_username, msg):
    for client_socket, username in clients:
        try:
            if username != sender_username:
                client_socket.send(f"[{sender_username}] {msg}".encode('utf-8'))
        except BrokenPipeError:
            print(f"Client {username} disconnected unexpectedly.")
            clients.remove((client_socket, username))

clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

server_ip = get_server_ip()  # Get the IP address of the server
print(f"[LISTENING] Server is listening on {server_ip}:{PORT}")

while True:
    client_socket, _ = server.accept()
    username = client_socket.recv(1024).decode('utf-8')
    clients.append((client_socket, username))
    thread = threading.Thread(target=handle_client, args=(client_socket, username))
    thread.start()
