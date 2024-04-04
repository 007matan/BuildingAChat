import threading
import socket
import argparse
import os
import sys
import tkinter as tk

"""
Class Send:
This class provides functionality for connecting to a chat server and sending messages to the server.
    ...
    Constructor
    -------
    __init__(self, host, port)
    The constructor for the Send class. It initializes
    the name (str) : provided by the user
    and sock address : the connected sock object.
    ...
    Methods
    -------
    run(self)
        Listen to the user input from the command line and send it to the server
        if we type "Quit" we leave the chatroom by sending message to the server and closing the connection.
    ...
    Functionality
    -------    
    The Client class provides functionality for connecting to a chat server and sending messages to the server.
    Messages typed by the user are sent to the server for broadcasting to other clients.
    The client's name is included in the messages sent to the server to identify the sender.
    This class utilizes multithreading to handle both sending and receiving messages simultaneously.
    It relies on the socket and threading modules for communication and concurrency.
"""


class Send(threading.Thread):


    def __init__(self, sock, name):

        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline().strip()

            # if we type "Quit" we leave the chatroom

            if message == "Quit":
                self.sock.sendall('Sever: {} has left the chat.'.format(self.name).encode('ascii'))
                break

            # send message to server for broadcasting

            else:
                self.sock.sendall('{}: {} '.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os.exit(0)


"""
Class Receive:
This class provides functionality for connecting to a chat server and receiving messages from the server.
    ...
    Constructor
    -------
    __init__(self, host, port)
    The constructor for the Receive class. It initializes
    
    ...
    Methods
    -------
    run(self)
    Receives data from the server and displays it in the gui
    ...
    
    Functionality
    -------    
    The Receive class provides functionality for receiving messages from the chat server and displaying them to the user.
    The run method continuously listens for incoming messages from the server.
    In the absence of a GUI, messages are printed to the command line, indicating the sender's name and the message content.
    The class monitors the connection to the server and handles disconnections.
    If the connection to the server is lost, it notifies the user and terminates the client application.
"""


class Receive(threading.Thread):

     def __init__(self, sock, name):
         super().__init__()
         self.sock = sock
         self.name = name
         self.messages = None

     def run(self):

         while True:
             message = self.sock.recv(1024).decode('ascii')

             if message:

                 if self.messages:
                     self.messages.insert(tk.END, message)
                     print('\r{}\n{}: '.format(message, self.name), end='')

                 else:
                     print('\r{}\n{}: '.format(message, self.name), end='')

             else:
                 print('\n No. We have lost connection to the server!')
                 print('\nQuitting...')
                 self.sock.close()
                 os._exit(0)


"""
Class Client:
This class defines a client for a Chat Room Simulation.
    ...
    Constructor
    -------
    __init__(self, host, port)
    The constructor for the Client class. It initializes
     
    ...
    Methods
    -------
    start(self)
    Establishes a connection to the chat server, initializes user settings,
    and starts send and receive threads for message exchange.
    The function returns Receive: An instance of the Receive class responsible for receiving messages from the server.
    
    send(self, textInput)
    The function send this input text date from the gui and this methos will be bound to the text input,
    and send message to the server for broadcasting.
    ...
    Functionality
    -------    
    Management of client-server connection and integration of GUI, 
    initializes a socket connection with the specified host and port to establish communication with the chat server.
    Upon successful connection, the user is prompted to enter their name, which is used to identify them in the chat room.
    The class manages sending and receiving messages concurrently by creating separate threads for each operation.
    Messages sent by the user are displayed in the chat interface, allowing for real-time communication with other users in the chat room.
"""


class Client:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):

        print ('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))

        print ('successfully connected to {}:{}\n'.format(self.host, self.port))

        self.name = input('Your name: \n')

        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads

        send  = Send(self.sock, self.name)

        receive = Receive(self.sock, self.name)

        send.start()

        receive.start()

        self.sock.sendall('Server: {} has joined the chat. say Hi!'.format(self.name).encode('ascii'))
        print("\rReady! Leave the chatroom anytime by typing 'Quit'\n")
        print('{}: '.format(self.name), end='')

        return receive


    def send(self, textInput):

        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))


        if message == "Quit":
            self.sock.sendall('Server: {} has left the chat.' .format(self.name).encode('ascii'))

            print('\nQuitting...')
            self.sock.close()
            os.exit(0)

        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))


def main(host, port):
    # initialize and run GUI application

    client = Client(host, port)
    receive = client.start()

    window = tk.Tk()
    window.title("Chatroom")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    receive.messages = messages

    fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda x: client.send(textInput))
    textInput.insert(0, "Write your message here.")

    btnSend = tk.Button(
        master=window,
        text='Send',
        command=lambda: client.send(textInput)
    )

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(0, minsize=200, weight=0)

    window.mainloop()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')

    args = parser.parse_args()

    main(args.host, args.p)