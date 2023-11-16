import threading
import socket

host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
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
            broadcast(f'{nickname} left the chat!'.encode('ascii'), chatrooms[room])
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Send acknowledgment for NICK
        client.send('ACK_NICK'.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Send acknowledgment for ROOM
        client.send('ACK_ROOM'.encode('ascii'))

        room = client.recv(1024).decode('ascii')
        if room not in chatrooms:
            chatrooms[room] = []

        chatrooms[room].append(client)
        print(f'These are the chatrooms: {chatrooms}!')

        print(f'Nickname of new client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'), room)
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client, room))
        thread.start()

receive()
