import socket
import threading


# Server settings
HOST = '10.33.155.108'  # Replace with server's IP address if needed
PORT = 55271 

# Client connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to send messages to the server
def send_message(msg):
    client.send(msg.encode('utf-8'))

# Function to receive messages from the server
def receive_messages(client, on_message_callback):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                on_message_callback(message)
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            client.close()
            break


# Start listening for messages
def start_receiving(client, on_message_callback):
    thread = threading.Thread(target=receive_messages, args=(client, on_message_callback))
    thread.daemon = True
    thread.start()



def close_client(client):
    try:
        client.close()
    except Exception as e:
        print(f"Error closing client: {e}")
