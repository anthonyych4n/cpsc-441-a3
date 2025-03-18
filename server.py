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

class PandaServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Format: {client_socket: panda_name}
        self.lock = threading.Lock()

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
            with self.lock:
                self.clients[client] = name
            self.broadcast(f"{name} has joined the grove! 🌿", sender=client)
            while True:
                message = client.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                if message == "@leaves":
                    self.remove_client(client)
                    break
                elif message == "@grove":
                    names = ", ".join(self.clients.values())
                    client.send(f"Current pandas: {names} 🎍".encode('utf-8'))
                elif message == "@bamboo":
                    fact = random.choice(PANDA_FACTS)
                    client.send(f"Panda Fact: {fact} 🌱".encode('utf-8'))
                else:
                    self.broadcast(f"{name}: {message}", sender=client)
        except:
            self.remove_client(client)

if __name__ == "__main__":
    server = PandaServer()
    server.start()