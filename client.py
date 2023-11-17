import random
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from threading import Thread
import socket


class ChatClientGUI:
    def __init__(self, root):

        self.root = root
        self.root.title(str(room)) #Creates a window named after the chat room


        self.message_entry = tk.Entry(root, width=50) #Create a text box where you can write messages
        self.message_entry.bind("<Return>", self.send_message) #Sends message if you click enter

        self.chat_display = scrolledtext.ScrolledText(root, width=60, height=20) #Creates a text window with scrollable text
        self.chat_display.configure(state='disabled') #Makes sure you cant change anything by typing in the window

        self.disconnect_button = tk.Button(root, text="Disconnect", state='disabled',
                                           command=self.disconnect_from_server) #Button that disconnects you

        # Send button
        self.send_button = tk.Button(root, text="Send", state='disabled', command=self.send_message) #Send if you press


        # Formatting of the window components
        self.message_entry.grid(row=2, column=0, padx=10, pady=10)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)
        self.disconnect_button.grid(row=1, column=0, padx=10, pady=5)
        self.send_button.grid(row=2, column=1, padx=10, pady=10)

        # Initialize all the variables
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = nickname
        self.room = room
        self.nickname_colors = {} #Directory that will store every nickname and give it a corresponding color.

        self.client_socket.connect(("127.0.0.1", 55555)) #Connect to the correct server

        self.client_socket.recv(1024)
        self.client_socket.send(self.nickname.encode('ascii'))
        self.client_socket.recv(1024)
        self.client_socket.send(self.room.encode('ascii'))

        self.disconnect_button['state'] = 'normal'
        self.send_button['state'] = 'normal'

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def disconnect_from_server(self):
        try:
            self.client_socket.close()

            #Disable all buttons
            self.disconnect_button['state'] = 'disabled'
            self.send_button['state'] = 'disabled'


        except Exception as e:
            messagebox.showerror("Error", f"Error during disconnection: {str(e)}")

    def send_message(self, event=None):
        try:
            message = f'{self.nickname}: {self.message_entry.get()}' #Message format

            self.client_socket.send(message.encode('ascii'))
            self.message_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Error", f"Error sending message: {str(e)}")

    def receive(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode('ascii')
                self.display_message(message)
        except:
            messagebox.showinfo("Disconnected", "You have been disconnected from the server.")
            self.disconnect_from_server()

    def display_message(self, message):

        parts = message.split(': ', 1)

        # Check if the message format is as expected
        if len(parts) == 2:
            nickname, content = parts[0], parts[1]

            # Determine the color for the nickname (or generate a new color)
            color = self.nickname_colors.get(nickname) #If the nickname already has a color we write in that color
            if color is None:

                color = '#{:02x}{:02x}{:02x}'.format( #Get only the darker colors
                    random.randint(0,190),
                    random.randint(0,190),
                    random.randint(0, 190)
                ) #Get a random color

                self.nickname_colors[nickname] = color #Put the color and name in the directory.

            tag_name = f"{nickname}_tag"
            # Configure the tag for the nickname with the determined color
            self.chat_display.tag_configure(tag_name, foreground=color)

            self.chat_display.configure(state='normal')
            self.chat_display.insert('end', message + '\n', tag_name) #Write in color
            self.chat_display.yview('end')
            self.chat_display.configure(state='disabled')

    def leave(self):
        self.client_socket.close()
        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    #LEt use choose nickname and room
    nickname = input("Choose a nickname: ")
    room = input("Which chatroom do you want to join? ")

    gui = ChatClientGUI(root)
    gui.nickname = nickname
    gui.room = room

    root.mainloop()
