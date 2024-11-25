import socket
import threading

# Server configuration
HOST = '10.33.155.108'  # Bind to all available interfaces
PORT = 55271      # Port to listen on

# List to store connected clients
clients = []

# Broadcast message to all connected clients
def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                clients.remove(client_socket)

# Handle communication with a single client
def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received from {client_address}: {message.decode('utf-8')}")
            broadcast(message, sender_socket=client_socket)
    except Exception as e:
        print(f"Error with client {client_address}: {e}")
    finally:
        print(f"Closing connection with {client_address}")
        clients.remove(client_socket)
        client_socket.close()

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started. Listening on {HOST}:{PORT}...")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
