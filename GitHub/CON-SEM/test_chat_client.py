import socket
import threading
import time

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Port used by server

def run_test_client(name, messages):
    """Connects to the chat server, sends messages, and prints received messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"[{name}] Received: {message}")
            except ConnectionAbortedError:
                break

    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Send messages from this test client
    for msg in messages:
        print(f"[{name}] Sending: {msg}")
        client_socket.send(f"{name}: {msg}".encode('utf-8'))
        time.sleep(1)  # Wait between messages

    # Close the connection after sending all messages
    time.sleep(2)
    client_socket.close()
    print(f"[{name}] Disconnected.")

# Test parameters
client1_messages = ["Hello!", "How are you?", "Testing message flow.", "Bye!"]
client2_messages = ["Hi everyone!", "Testing chat server...", "Sending more data...", "End test."]

# Run two test clients
thread1 = threading.Thread(target=run_test_client, args=("Client1", client1_messages))
thread2 = threading.Thread(target=run_test_client, args=("Client2", client2_messages))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Test complete.")
