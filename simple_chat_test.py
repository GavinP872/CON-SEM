import socket

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Port the server is running on

def simple_chat():
    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            print("Connected to the chat server.")
            
            # Get a message from the user
            user_message = input("You: ")
            
            # Send the message to the server
            client_socket.send(user_message.encode('utf-8'))
            
            # Wait for the server's response
            server_response = client_socket.recv(1024).decode('utf-8')
            print("Server:", server_response)
            
            print("Chat ended.")
        
        except ConnectionRefusedError:
            print("Failed to connect to the server. Please make sure the server is running.")

# Run the simple chat test
if __name__ == "__main__":
    simple_chat()
