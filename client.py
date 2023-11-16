import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

nickname = input("Choose a nickname: ")
room = input("Which chatroom do you want to join? (Default is named 'All') ")

# Receive acknowledgment for NICK
client.recv(1024)

# Send nickname
client.send(nickname.encode('ascii'))

# Receive acknowledgment for ROOM
client.recv(1024)

# Send room
client.send(room.encode('ascii'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            print("An error has occurred!")
            client.close()
            break

def write():
    while True:
        writing = input('')
        if writing.lower() == 'exit':
            leave()
        message = '{}: {}'.format(nickname, writing)
        client.send(message.encode('ascii'))

def leave():
    client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
