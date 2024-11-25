import socket
import threading

clients = []  # List to store connected clients

def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")
    while True:  # Keep the connection open for this client
        try:
            # Receive data from the client
            message = client_socket.recv(1024).decode("utf-8")
            if not message:  # Empty message means the client disconnected
                print(f"Client {client_address} disconnected.")
                break
            print(f"Received from {client_address}: {message}")
            
            # Echo the message back to all connected clients
            for sock in clients:
                if sock != client_socket:  # Don't echo to the sender
                    sock.sendall(f"From {client_address}: {message}".encode("utf-8"))
        except ConnectionResetError:
            print(f"Connection reset by {client_address}. Closing.")
            break
        except Exception as e:
            print(f"Error with {client_address}: {e}")
            break

    # Remove the client and close the socket
    clients.remove(client_socket)
    client_socket.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)

def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.33.155.108", 55271))
    server.listen(5)
    print("Server started. Waiting for connections...")
    accept_connections(server)
