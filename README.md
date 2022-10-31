# socket game for csci70

## setup
---

### clone the repo
```sh
git clone git@github.com:jamesesguerra/python_socket_game.git
```

### cd into folder
```sh
cd python_socket_game
```

### change file permissions to run files as scripts (optional)
```sh
chmod +x server.py client.py
```

## usage
---

### server

run `server.py` with the `-h` flag to view options
```sh
./server.py -h
```

start the server
```sh
./server.py --port 4000
```

example: starting the server on port 4000 only accepting connections from the same host
```sh
./server.py --host 127.0.0.1 --port 4000
```

### client

run `client.py` with the `-h` flag to view options
```sh
./client.py -h
```

connect to the server
```sh
./client.py --port 4000
```

example: connecting to a server with IP 192.168.254.108 running on port 4000
```sh
./client.py --host 192.168.254.108 --port 4000
```

