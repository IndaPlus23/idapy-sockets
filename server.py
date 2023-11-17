import threading
import socket


HOST = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
chatrooms = {'All': [], 'Main': []}

def broadcast(message, chatroom):
    for client in chatroom:
        try:
            client.send(message)
        except:
            pass

def handle(client, room):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, chatrooms[room])
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'), chatrooms[room])
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        try:

            # Send acknowledgment for NICK
            client.send('ACK_NICK'.encode('utf-8'))

            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            # Send acknowledgment for ROOM
            client.send('ACK_ROOM'.encode('utf-8'))

            room = client.recv(1024).decode('utf-8')
            if room not in chatrooms:
                chatrooms[room] = []

            chatrooms[room].append(client)
            print(f'These are the chatrooms: {chatrooms}!')

            print(f'Nickname of new client is {nickname}!')
            broadcast(f'{nickname} joined the chat!'.encode('utf-8'), room)
            client.send('Connected to the server!'.encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client, room))
            thread.start()

        except (ConnectionResetError, ConnectionAbortedError):
            # Handle the exception (e.g., print a message or clean up)
            print("Client connection error")
receive()
