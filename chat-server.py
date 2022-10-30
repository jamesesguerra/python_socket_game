import threading
import socket

host = ''
port = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# send msg to all clients connected to server
def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast(f'{nickname} left the chat.'.encode('ascii'))
			nicknames.remove(nickname)
			break

def receive():
	while True:
		client, addr = server.accept()
		print(f'Established connection with {str(addr)}')

		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)
		
		broadcast(f'{nickname} joined the chat'.encode('ascii'))
		client.send('\nConnected to the server.'.encode('ascii'))

		t = threading.Thread(target=handle, args=(client,))
		t.start()

print(f'Server listening on port {port}...')
receive()
