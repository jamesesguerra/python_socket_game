def broadcast(message, clients):
    for client in clients:
        client["client_ID"].sendall(message)