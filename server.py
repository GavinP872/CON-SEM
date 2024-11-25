import socket
import threading

# Server configuration
HOST = '10.33.155.108'  # Server address (localhost for testing)
PORT = 55271        # Port to bind server

# List to store connected client sockets
clients = []

# Function to handle individual client communication
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received (server): {message}")
                # Broadcast the message to other connected clients
                broadcast(message, client_socket)
            else:
                break
        except:  # Handle any errors (e.g., client disconnects unexpectedly)
            break
    
    # Remove client socket from the list and close connection
    clients.remove(client_socket)
    client_socket.close()

# Function to send messages to all connected clients except the sender
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Skip the sender
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                clients.remove(client)


# Function to start the server and accept connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Bind server to specified HOST and PORT
    server_socket.listen(5)  # Allow up to 5 queued connections
    print("Server started. Waiting for connections...")

    while True:
        # Accept new client connection
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)  # Add client socket to list
        # Create a new thread to handle this client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

start_server()
