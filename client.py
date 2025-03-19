import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')  # Increased buffer for ASCII
            print(message)
        except:
            print("Disconnected from the server.")
            client.close()
            break

def main():
    host = 'localhost'
    port = 5555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    name = input(client.recv(1024).decode('utf-8'))
    client.send(name.encode('utf-8'))
    print(f"Connected as {name}! Type '@leaves' to exit.")
    threading.Thread(target=receive_messages, args=(client,)).start()
    while True:
        message = input()
        if message.lower() == "@leaves":
            client.send(message.encode('utf-8'))
            break
        client.send(message.encode('utf-8'))
    client.close()

if __name__ == "__main__":
    main()