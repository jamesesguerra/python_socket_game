import socket
import threading


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")

            print(message == "RPS")
            
            # server asking for username
            if message == "USER":
                client.send(username.encode("ascii"))
            
            # rock paper scissors
            elif message == "RPS":
                user_action = input("\nEnter a choice (rock, paper, or scissors): ")
                client.send(user_action.encode("ascii"))

            else:
                print(message)
        except:
            print('An error occured')
            client.close()
            break


def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))


if __name__ == "__main__":
    username = input("Choose a username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 65432))

    t1 = threading.Thread(target=receive)
    t1.start()

    t2 = threading.Thread(target=write)
    t2.start()
