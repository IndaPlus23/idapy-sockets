import threading
import socket

host = "127.0.0.1"  # Localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()  # Listen for incoming connections

clients = []  # New clients in this list
nicknames = []  # Nicknames of the clients in this list


def broadcast(message):
    for client in clients:
        client.send(message)  # Broadcas a message to all the clients in the client list


def handle(client):  # Run the function on all client to get the messages

    while True:

        try:  # If you get a message send to all

            message = client.recv(1024)
            broadcast(message)

        except:

            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))  # If someone leaves the chat
            nicknames.remove(nickname)
            break


def recieve():  # Recieve new clients

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of new client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


recieve()



