#!/usr/bin/env python3

import concurrent.futures
import time

from utils import broadcast


# rock paper scissors
choices = []

def handle_choice(client):
    try:
        client_choice = client["client_ID"].recv(1024).decode("ascii")
        choices.append(client_choice)
        client["client_ID"] \
            .sendall(f"You chose {client_choice}, waiting for results..."
            .encode("ascii"))
        return choices
    except:
        client["client_ID"].close()


def check_for_winner(choices, clients):
    player1 = clients[0]["username"]
    player2 = clients[1]["username"]
    player1_choice = choices[0]
    player2_choice = choices[1]

    print(player1_choice)
    print(player2_choice)

    if player1_choice == player2_choice:
        choices.clear()
        broadcast(f"Both players selected {player1_choice}, trying again..."
            .encode("ascii"), clients)
        time.sleep(1)
        return None
    
    elif player1_choice == "rock":
        if player2_choice == "scissors":
            broadcast(f"Rock beats scissors, {player1} will guess first."
                .encode("ascii"), clients)
            return clients[0]
        else:
            broadcast(f"Paper beats rock, {player2} will guess first."
                .encode("ascii"), clients)
            return clients[1]
    
    elif player1_choice == "paper":
        if player2_choice == "rock":
            broadcast(f"Paper beats rock, {player1} will guess first."
                .encode("ascii"), clients)
            return clients[0]
        else:
            broadcast(f"Scissors beats paper, {player2} will guess first."
                .encode("ascii"), clients)
            return clients[1]
    
    elif player1_choice == "scissors":
        if player2_choice == "paper":
            broadcast(f"Scissors beats paper, {player1} will guess first."
                .encode("ascii"), clients)
            return clients[0]
        else:
            broadcast(f"Rock beats paper, {player2} will guess first."
                .encode("ascii"), clients)
            return clients[1]


def rock_paper_scissors(clients):
    winner = None

    while winner is None:
        broadcast("RPS".encode("ascii"), clients)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(handle_choice, clients)
        winner = check_for_winner(list(results)[1], clients)

    return winner


# number guessing game
def guessing_game(winner, clients):
    print(f"Congrats {winner['username']}")


def start_game(clients):
    winner = rock_paper_scissors(clients)
    guessing_game(winner, clients)