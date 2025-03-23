import socket
import threading

def receive_messages(client, running):
    while running.is_set():
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break
    print("\nDisconnected from the server.")
    running.clear()
    client.close()

def main():
    host = 'localhost'
    port = 3000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    running = threading.Event()
    running.set()
    
    try:
        client.connect((host, port))
        name = input(client.recv(1024).decode('utf-8'))
        client.send(name.encode('utf-8'))
        print(f"Connected as {name}! Type '@leaves' to exit.")
        
        receiver = threading.Thread(target=receive_messages, args=(client, running))
        receiver.start()
        
        while running.is_set():
            try:
                message = input()
                if message.lower() == "@leaves":
                    client.send(message.encode('utf-8'))
                    break
                client.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                client.send("@leaves".encode('utf-8'))
                break
                
    except Exception as e:
        print(f"Connection error: {str(e)}")
    finally:
        running.clear()
        try:
            client.shutdown(socket.SHUT_RDWR)
        except:
            pass
        client.close()
        receiver.join(timeout=1)

if __name__ == "__main__":
    main()