#!/usr/bin/env python3

import socket
import threading


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            
            # server asking for username
            if message == "USER":
                client.sendall(username.encode("ascii"))
            
            # rock paper scissors
            elif "RPS" in message:
                user_action = input("\nEnter a choice (rock, paper, or scissors): ")
                client.sendall(user_action.encode("ascii"))

            else:
                print(message)
        except:
            print('An error occured')
            client.close()
            break


# def write():
#     while True:
#         message = f'{username}: {input("")}'
#         client.send(message.encode('ascii'))


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 65432))

    username = input("Choose a username: ")

    t1 = threading.Thread(target=receive)
    t1.start()

    # t2 = threading.Thread(target=write)
    # t2.start()
