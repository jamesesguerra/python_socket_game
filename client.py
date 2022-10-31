#!/usr/bin/env python3

import argparse
import socket
import threading


def receive():
    end = False
    while not end:
        try:
            message = client.recv(1024).decode("ascii")
            
            # username
            if message == "USER":
                client.sendall(username.encode("ascii"))
            
            # rock paper scissors
            elif message == "RPS":
                user_action = input("\nEnter a choice \
                    (rock, paper, or scissors): ")
                client.sendall(user_action.encode("ascii"))

            # number guessing game
            elif message == "NUM":
                user_guess = input("\nEnter a number between 1 and 100: ")
                client.sendall(user_guess.encode("ascii"))

            # game end
            elif message == "END":
                end = True
                
            else:
                print(message)
        except:
            client.close()
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for guessing game")
    parser.add_argument("--host",
        help="IP of host to connect to", default="127.0.0.1")
    parser.add_argument("--port", "-p",
        help="Port on host to connect to", default=65432)
    args = parser.parse_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.host, int(args.port)))

    username = input("Choose a username: ")
    t = threading.Thread(target=receive)
    t.start()
