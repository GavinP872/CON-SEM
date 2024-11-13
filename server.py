import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost for testing, change to your server's IP to allow remote connections
PORT = 5000

clients = []  # List to store connected clients

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    # Handle the client’s messages
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
                # Broadcast message to all clients except the sender
                broadcast(message, client_socket)
            else:
                break
        except:
            break
    
    # Remove client when they disconnect
    clients.remove(client_socket)
    client_socket.close()

# Broadcast a message to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server started. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

start_server()
