import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Replace with server's IP address if needed
PORT = 5000

# Client connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to send messages to the server
def send_message(msg):
    client.send(msg.encode('utf-8'))

# Function to receive messages from the server
def receive_messages(on_message_callback):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            on_message_callback(message)
        except:
            client.close()
            break 

# Start listening for messages
def start_receiving(on_message_callback):
    thread = threading.Thread(target=receive_messages, args=(on_message_callback,))
    thread.start()
