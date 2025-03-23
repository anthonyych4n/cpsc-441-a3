import socket
import threading

# Function to handle receiving messages from the server
def receive_messages(client, running):
    while running.is_set():  # Continue receiving messages while the client is running
        try:
            # Receive and decode messages from the server
            message = client.recv(4096).decode('utf-8')
            if not message:  # If no message is received, exit the loop
                break
            print(message)  # Print the received message
        except:
            break  # Exit the loop if an error occurs
    print("\nDisconnected from the server.")  # Notify the user of disconnection
    running.clear()  # Stop the running event
    client.close()  # Close the client socket

# Main function to handle client-side operations
def main():
    host = 'localhost'  # Server hostname or IP address
    port = 3000  # Server port number
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    running = threading.Event()  # Create an event to manage the running state
    running.set()  # Set the event to indicate the client is running
    
    try:
        # Connect to the server
        client.connect((host, port))
        # Receive the server's prompt for a name and send the user's input
        name = input(client.recv(1024).decode('utf-8'))
        client.send(name.encode('utf-8'))
        print(f"Connected as {name}! Type '@leaves' to exit.")  # Inform the user of successful connection
        
        # Start a thread to handle receiving messages from the server
        receiver = threading.Thread(target=receive_messages, args=(client, running))
        receiver.start()
        
        # Main loop to send messages to the server
        while running.is_set():
            try:
                message = input()  # Get user input
                if message.lower() == "@leaves":  # Check if the user wants to exit
                    client.send(message.encode('utf-8'))  # Notify the server of disconnection
                    break
                client.send(message.encode('utf-8'))  # Send the message to the server
            except KeyboardInterrupt:  # Handle Ctrl+C gracefully
                client.send("@leaves".encode('utf-8'))  # Notify the server of disconnection
                break
                
    except Exception as e:
        # Handle connection errors
        print(f"Connection error: {str(e)}")
    finally:
        # Clean up resources when exiting
        running.clear()  # Stop the running event
        try:
            client.shutdown(socket.SHUT_RDWR)  # Shutdown the socket
        except:
            pass
        client.close()  # Close the client socket
        receiver.join(timeout=1)  # Wait for the receiver thread to finish

# Entry point of the script
if __name__ == "__main__":
    main()