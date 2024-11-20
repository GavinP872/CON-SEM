import threading
from chat_functions import send_message, start_receiving

# Simulate client 1 sending and receiving messages
def simulate_client1():
    def display_message(message):
        print(f"Client 1 received: {message}")
    
    # Start receiving messages in a separate thread
    start_receiving(display_message)

    # Send a test message
    send_message("Hello from Client 1!")

# Simulate client 2 sending and receiving messages
def simulate_client2():
    def display_message(message):
        print(f"Client 2 received: {message}")

    # Start receiving messages in a separate thread
    start_receiving(display_message)

    # Send a test message
    send_message("Hello from Client 2!")

# Run both clients in separate threads to mimic real-world conditions
if __name__ == "__main__":
    thread1 = threading.Thread(target=simulate_client1)
    thread2 = threading.Thread(target=simulate_client2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
