#!/usr/bin/env python3

import socket

from utils import broadcast
from games import start as start_game


def receive():
    while True:
        client, addr = server.accept()
        print(f"Established connection with {str(addr)}")
        
        client.sendall("USER".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        clients.append({ "client_ID": client, "username": username })

        broadcast(f"{username} joined.".encode("ascii"), clients)
        client.sendall("\nConnected to the server".encode("ascii"))

        if len(clients) < 2:
            client.sendall("\nWaiting for another player to join...".encode("ascii"))
        else:
            start_game(clients)


if __name__ == "__main__":
    host = ""
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []

    print(f"Server listening on port {port}...")
    receive()

