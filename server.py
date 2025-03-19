from datetime import datetime
import socket
import threading
import random

# Panda-themed configurations
PANDA_EMOJIS = ["🐼", "🎍", "🎋", "🌿", "🍃"]
PANDA_FACTS = [
    "Pandas spend around 14 hours a day eating bamboo!",
    "Baby pandas are born pink and weigh only about 100 grams!",
    "A group of pandas is called an embarrassment!",
    "Pandas can swim and are excellent tree climbers!",
    "There are only about 1,800 giant pandas left in the wild."
]

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
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Format: {client_socket: panda_name}
        self.lock = threading.Lock()
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
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started on {self.host}:{self.port} {PANDA_EMOJIS[0]}")
        while True:
            client, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def broadcast(self, message, sender=None):
        panda_emoji = random.choice(PANDA_EMOJIS)
        decorated_message = f"{panda_emoji} {message}"
        with self.lock:
            for client in self.clients:
                if client != sender:
                    try:
                        client.send(decorated_message.encode('utf-8'))
                    except:
                        self.remove_client(client)

    def remove_client(self, client):
        with self.lock:
            if client in self.clients:
                name = self.clients[client]
                del self.clients[client]
                self.broadcast(f"{name} has left the bamboo grove! 🎋", sender=client)
                client.close()

    def handle_client(self, client):
        try:
            client.send("Enter your panda name: ".encode('utf-8'))
            name = client.recv(1024).decode('utf-8').strip()
            client.send(PANDA_ASCII["welcome"].encode('utf-8'))
            with self.lock:
                self.clients[client] = name
            self.broadcast(f"{name} has joined the grove! 🌿", sender=client)
            self.write_log(f"User joined: {name}")  # Existing log
            
            while True:
                message = client.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                 # Log the raw message before processing
                self.write_log(f"Message from {name}: {message}")
                if message == "@leaves":
                    self.remove_client(client)
                    break
                elif message == "@grove":
                    names = ", ".join(self.clients.values())
                    client.send(f"Current pandas: {names} 🎍".encode('utf-8'))
                elif message == "@bamboo":
                    fact = random.choice(PANDA_FACTS)
                    client.send(f"Panda Fact: {fact} 🌱".encode('utf-8'))
                elif message in PANDA_ASCII:
                    self.broadcast(f"\n{PANDA_ASCII[message]}\n{name} {message}s!")
                    continue
                else:
                    self.broadcast(f"{name}: {message}", sender=client)
        except Exception as e:
            self.write_log(f"Error with {name}: {str(e)}")
        finally:
            self.write_log(f"User left: {name}")
            
    def __del__(self):
        self.log_file.close()

if __name__ == "__main__":
    server = PandaServer()
    server.start()