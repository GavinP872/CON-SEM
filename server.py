import socket

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Same port as client

# Start the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server started. Waiting for connections...")

    # Accept a single connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        
        # Receive a message from the client
        message = conn.recv(1024).decode('utf-8')
        if message:
            print("Received from client:", message)
            
            # Send a response back to the client
            response = "Message received: " + message
            conn.sendall(response.encode('utf-8'))

        # Close the connection after one message
        print("Closing connection with client.")
