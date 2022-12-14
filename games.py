#!/usr/bin/env python3

import concurrent.futures
import random
import time

from utils import broadcast


# rock paper scissors
choices = []

def handle_choice(client):
    try:
        client_choice = client["client_ID"].recv(1024).decode("ascii")
        choices.append({ 
            "client_choice": client_choice, 
            "username": client["username"] 
        })
        client["client_ID"] \
            .sendall(f"You chose {client_choice}, waiting for results..."
            .encode("ascii"))
        return choices
    except:
        client["client_ID"].close()


def check_for_winner(choices, clients):
    player1 = clients[0]["username"]
    player2 = clients[1]["username"]
    player1_choice = choices[0]["client_choice"] \
        if choices[0]["username"] == player1 else choices[1]["client_choice"]
    player2_choice = choices[0]["client_choice"] \
        if choices[0]["username"] != player1 else choices[1]["client_choice"]

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
        broadcast("\nStarting a game of rock paper scissors to decide who guesses first..."
            .encode("ascii"), clients)
        time.sleep(0.5)
        broadcast("RPS".encode("ascii"), clients)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(handle_choice, clients)
        winner = check_for_winner(list(results)[1], clients)

    return winner


# number guessing game
def guess(client, clients, num):
    time.sleep(0.5)
    client["client_ID"].sendall("NUM".encode("ascii"))
    return check_guess(client, clients, num)


def check_guess(client, clients, num):
    try:
        guess = int(client["client_ID"].recv(1024).decode("ascii"))
        
        if guess < num:
            broadcast(f"{client['username']}'s guess ({guess}) is too low."
                .encode("ascii"), clients)
        elif guess > num:
            broadcast(f"{client['username']}'s guess ({guess}) is too high."
                .encode("ascii"), clients)
        else:
            broadcast(f"{client['username']} guessed the number {num} correctly! \
                \nThank you for playing."
                .encode("ascii"), clients)
            return client
    except:
        client["client_ID"].close()


def guessing_game(winner, clients):
    player1 = clients[0] if clients[0] == winner else clients[1]
    player2 = clients[0] if clients[0] != winner else clients[1]

    random_num = random.randint(1, 100)
    broadcast("\nI'm thinking of a number between 1 and 100..."
        .encode("ascii"), clients)

    while True:
        player2["client_ID"].sendall(f"\n{player1['username']} is guessing..."
            .encode("ascii"))
        winner = guess(player1, clients, random_num)
        if winner: break

        player1["client_ID"].sendall(f"\n{player2['username']} is guessing..."
            .encode("ascii"))
        winner = guess(player2, clients, random_num)
        if winner: break

    time.sleep(0.5)
    broadcast("END".encode("ascii"), clients)


# start
def start(clients):
    winner = rock_paper_scissors(clients)
    guessing_game(winner, clients)