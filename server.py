#!/usr/bin/env python3

import socket
import threading

from utils import broadcast
from games import start_game


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
        
        client.sendall("USER".encode("ascii"))
        username = client.recv(1024).decode("ascii")
        clients.append(client)
        usernames.append(username)

        broadcast(f"{username} joined.".encode("ascii"), clients)
        client.sendall("\nConnected to the server".encode("ascii"))

        if len(clients) < 2:
            client.sendall("\n\nWaiting for another player to join...".encode("ascii"))
        else:
            # broadcast("\n\nStarting game...\n".encode("ascii"), clients)

            start_game(clients, usernames)


if __name__ == "__main__":
    host = ""
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    usernames = []

    print(f"Server listening on port {port}...")
    receive()

