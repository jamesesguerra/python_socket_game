#!/usr/bin/env python3

import argparse
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
            client.sendall("\nWaiting for another player to join..."
                .encode("ascii"))
        else:
            start_game(clients)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server for guessing game")
    parser.add_argument("--host", 
        help="Hosts to accept connections from \
            (leave blank to accept connections from any host)",
        default="")
    parser.add_argument("--port", "-p",
        help="Port to bind socket to", default=65432)
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((args.host, int(args.port)))
    server.listen()

    clients = []
    print(f"Server listening on port {args.port}...")
    receive()

