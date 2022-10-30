import socket
import threading

from utils import broadcast
from games import rock_paper_scissors


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, clients)
        except:
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        client, addr = server.accept()
        print(f"Established connection with {str(addr)}")
        
        client.send("USER".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        clients.append(client)

        broadcast(f"{username} joined.".encode("ascii"), clients)
        client.send("\nConnected to the server".encode("ascii"))

        if len(clients) < 2:
            client.send("\n\nNeed one more player!".encode("ascii"))
        else:
            broadcast("\n\nStarting game...\n".encode("ascii"), clients)

            rock_paper_scissors(clients)


        t = threading.Thread(target=handle, args=(client,))
        t.start()


if __name__ == "__main__":
    host = ""
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []

    print(f"Server listening on port {port}...")
    receive()

