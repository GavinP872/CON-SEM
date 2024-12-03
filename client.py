import socket
import threading


# Server configuration
HOST = '10.187.122.195'  # Server's external IP
PORT = 50505             # Selected available port


NAME = " "
# Receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving messages: {e}")
    finally:
        client_socket.close()

# Start the client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")

        # Start a thread to receive messages
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        # Send messages to the server
        while True:
            message = NAME + input()
            if message.lower() == "exit":
                break
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error connecting to server: {e}")
    finally:
        client_socket.close()
        print("Disconnected from the server.")



if __name__ == "__main__":
    start_client()

