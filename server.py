from datetime import datetime
import socket
import threading
import random
import sys

# Panda-themed configurations
PANDA_EMOJIS = ["🐼", "🎍", "🎋", "🌿", "🍃"]  # Emojis used for decorating messages
PANDA_FACTS = [  # Fun facts about pandas
    "Pandas spend around 14 hours a day eating bamboo!",
    "Baby pandas are born pink and weigh only about 100 grams!",
    "A group of pandas is called an embarrassment!",
    "Pandas can swim and are excellent tree climbers!",
    "There are only about 1,800 giant pandas left in the wild."
]

# ASCII art for specific commands
PANDA_ASCII = {
    "welcome": r"""
   (\_/)  
  (•.•)  
  / >🎍 Welcome to Panda Chat!
    """,
    "@hug": r"""
  c(_)🥰 Hugs for everyone!
    (\ 
     \ ) 
    """,
    "@love": r"""
   ♥‿♥  
  /🎋\  Love from the pandas!
    """,
    "@sad": r"""
  (>_<)  
  /🎍\  Bamboo shortage sadness
    """
}

class PandaServer:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()
        self.running = True  # Flag to control server operation
        self.setup_logging()

    def setup_logging(self):
        self.log_file = open("panda_server.log", "a")
        self.write_log("Server initialized")

    def write_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        with self.lock:
            self.log_file.write(log_entry)
            self.log_file.flush()


    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            self.server.settimeout(2)  # Allows periodic check of running flag
            print(f"Server started on {self.host}:{self.port} {PANDA_EMOJIS[0]}")
            
            while self.running:
                try:
                    client, addr = self.server.accept()
                    thread = threading.Thread(target=self.handle_client, args=(client,))
                    thread.daemon = True
                    thread.start()
                except socket.timeout:
                    continue  # Timeout to periodically check running flag
        except Exception as e:
            if self.running:  # Only log if not intentional shutdown
                self.write_log(f"Server error: {str(e)}")
            print(f"Server error: {str(e)}")
        finally:
            self.shutdown()            

    def shutdown(self):
        """Gracefully shut down the server"""
        if not self.running:
            return
        
        self.running = False
        print("\nInitiating graceful shutdown...")
        
        with self.lock:
            # Close all client connections
            for client in self.clients.copy():
                try:
                    client.send("Server is shutting down! 🎋".encode('utf-8'))
                    client.close()
                except:
                    pass
            self.clients.clear()
        
        # Close server socket
        try:
            self.server.shutdown(socket.SHUT_RDWR)
            self.server.close()
        except:
            pass
        
        # Close log file
        self.log_file.close()
        print("Server shut down gracefully. Goodbye! 🐼")
        sys.exit(0)

    def broadcast(self, message, sender=None):
        # Send a message to all connected clients except the sender
        panda_emoji = random.choice(PANDA_EMOJIS)  # Add a random panda emoji to the message
        decorated_message = f"{panda_emoji} {message}"
        with self.lock:  # Ensure thread-safe access to the clients dictionary
            for client in self.clients:
                if client != sender:  # Skip the sender
                    try:
                        client.send(decorated_message.encode('utf-8'))  # Send the message
                    except:
                        self.remove_client(client)  # Remove client if sending fails

    def remove_client(self, client):
        # Remove a client from the server
        with self.lock:
            if client in self.clients:
                name = self.clients[client]  # Get the client's panda name
                del self.clients[client]  # Remove the client from the dictionary
                self.broadcast(f"{name} has left the bamboo grove! 🎋", sender=client)  # Notify others
                client.close()  # Close the client's connection

    def handle_client(self, client):
        # Handle communication with a connected client
        try:
            client.send("Enter your panda name: ".encode('utf-8'))  # Prompt for a panda name
            name = client.recv(1024).decode('utf-8').strip()  # Receive and store the panda name
            client.send(PANDA_ASCII["welcome"].encode('utf-8'))  # Send a welcome message
            with self.lock:
                self.clients[client] = name  # Add the client to the dictionary
            self.broadcast(f"{name} has joined the grove! 🌿", sender=client)  # Notify others
            self.write_log(f"User joined: {name}")  # Log the new connection
            
            while True:
                message = client.recv(1024).decode('utf-8').strip()  # Receive a message from the client
                if not message:
                    break  # Exit if the message is empty
                self.write_log(f"Message from {name}: {message}")  # Log the message
                if message == "@leaves":
                    self.remove_client(client)  # Remove the client if they leave
                    break
                elif message == "@grove":
                    # Send a list of connected pandas to the client
                    names = ", ".join(self.clients.values())
                    client.send(f"Current pandas: {names} 🎍".encode('utf-8'))
                elif message == "@bamboo":
                    # Send a random panda fact to the client
                    fact = random.choice(PANDA_FACTS)
                    client.send(f"Panda Fact: {fact} 🌱".encode('utf-8'))
                elif message in PANDA_ASCII:
                    # Broadcast a special ASCII message
                    self.broadcast(f"\n{PANDA_ASCII[message]}\n{name} {message}s!")
                    continue
                else:
                    # Broadcast a regular message
                    self.broadcast(f"{name}: {message}", sender=client)
        except Exception as e:
            self.write_log(f"Error with {name}: {str(e)}")  # Log any errors
        finally:
            self.write_log(f"User left: {name}")  # Log when the user disconnects

    def __del__(self):
        # Ensure the log file is closed when the server is destroyed
        self.log_file.close()

if __name__ == "__main__":
    server = PandaServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()