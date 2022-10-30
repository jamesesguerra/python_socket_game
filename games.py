#!/usr/bin/env python3

import concurrent.futures

from utils import broadcast


# rock paper scissors

choices = []

def handle_choice(client):
    try:
        client_choice = client.recv(1024).decode("ascii")
        choices.append(client_choice)
        client.sendall(f"You chose {client_choice}, waiting for results...".encode("ascii"))
        return choices
    except:
        client.close()


def check_for_winner(choices):
    print(choices[0], choices[1])


def rock_paper_scissors(clients, usernames):
    broadcast("RPS".encode("ascii"), clients)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(handle_choice, clients)

        check_for_winner(list(results)[1])


# number guessing game


# start game
def start_game(clients, usernames):
    rock_paper_scissors(clients, usernames)
    # number_guessing()