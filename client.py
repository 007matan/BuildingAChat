import threading
import socket
import argparse
import os
import sys
import openai
from MessageProtocol import MessageProtocol
import tkinter as tk
from enum import Enum
from openai import OpenAI
import requests

"""
ai_messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

# Set the API key
openai.api_key = ('')


client = OpenAI()

response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
  temperature=0.9,
  max_tokens=64,
  top_p=1,
  presence_penalty=0.6,
  stop=[" Human:", " AI:"]
)

URL = "https://api.openai.com/v1/chat/completions"

payload = {
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": f"What is the first computer in the world?"}],
"temperature" : 1.0,
"top_p":1.0,
"n" : 1,
"stream": False,
"presence_penalty":0,
"frequency_penalty":0,
}

headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {openai.api_key}"
}

response = requests.post(URL, headers=headers, json=payload, stream=False)
response.content
"""


"""
Class Send:
This class provides functionality for connecting to a chat server and
sending messages to the server.
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
        Listen to the user input from the command line and send it to
        the server if we type "Quit" we leave the chatroom by sending
        message to the server and closing the connection.
    ...
    Functionality
    -------    
    The Send class provides functionality for connecting to a chat server
    and sending messages to the server. Messages typed by the user are
    sent to the server for broadcasting to other clients. The client's
    name is included in the messages sent to the server to identify the
    sender. This class utilizes multithreading to handle both sending and
    receiving messages simultaneously. It relies on the socket and threading
    modules for communication and concurrency.
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
            encode_message = MessageProtocol.encode(message)

            if message == "Quit":
                self.sock.sendall('{} Sever: {} has left the chat.'.format(MessageProtocol.SYS_MSG, self.name).encode('ascii'))
                break

            # send message to server for broadcasting

            else:
                self.sock.sendall('{}: {} '.format(self.name, encode_message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os.exit(0)


"""
Class Receive:
This class provides functionality for connecting to a
chat server and receiving messages from the server.
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
    The Receive class provides functionality for receiving messages from the
    chat server and displaying them to the user. The run method continuously
    listens for incoming messages from the server. In the absence of a GUI,
    messages are printed to the command line, indicating the sender's name and
    the message content. The class monitors the connection to the server and
    handles disconnections. If the connection to the server is lost, it notifies
    the user and terminates the client application.
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
                     self.messages.configure(state='normal')  # Enable the widget for editing
                     self.messages.insert(tk.END, '{}\n'.format(message))  # Insert the message
                     self.messages.configure(state='disabled')  # Disable the widget to make it read-only

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
    The function returns Receive: An instance of the Receive class responsible
    for receiving messages from the server.
    
    send(self, textInput)
    The function send this input text date from the gui and this methos will
    be bound to the text input, and send message to the server for broadcasting.
    ...
    Functionality
    -------    
    Management of client-server connection and integration of GUI, initializes
    a socket connection with the specified host and port to establish communication
    with the chat server. Upon successful connection, the user is prompted to enter
    their name, which is used to identify them in the chat room. The class manages
    sending and receiving messages concurrently by creating separate threads for each operation.
    Messages sent by the user are displayed in the chat interface, allowing for
    real-time communication with other users in the chat room.
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


        username  = input('Your name: \n')
        while " " in username:
            print("Forbidden name {} - Name must not include space".format(username))
            username = input('Your name: \n')
        self.name = username

        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads

        send = Send(self.sock, self.name)

        receive = Receive(self.sock, self.name)


        send.start()

        receive.start()


        self.sock.sendall('{} Server: {} has joined the chat. say Hi!'.format(MessageProtocol.SYS_MSG, self.name).encode('ascii'))
        print("\rReady! Leave the chatroom anytime by typing 'Quit'\n")
        print('{}: '.format(self.name), end='')

        return receive


    def send(self, textInput):

        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.configure(state='normal')  # Enable the widget for editing
        self.messages.insert(tk.END, '{}: {}\n'.format(self.name, message))  # Insert the message
        self.messages.configure(state='disabled')  # Disable the widget to make it read-only


        if message == "Quit":
            self.sock.sendall('{} Server: {} has left the chat.' .format(MessageProtocol.SYS_MSG, self.name).encode('ascii'))

            print('\nQuitting...')
            self.sock.close()
            os.exit(0)

        else:
            encode_message = MessageProtocol.encode(message)
            self.sock.sendall('{}: {}'.format(self.name, encode_message).encode('ascii'))

class TypeOfService(Enum):
    EVERY_N_LINES = 1  # Type of service: response every N lines
    EVERY_N_SECS = 2  # Type of service: response every N secs


class AIClient:

    ROWS_AI_READ_EACH_TIME = 4  #
    CHARS_IN_ROW = 30  # amount of chars in each row in chat

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages = None
        self.typeOfService = TypeOfService.EVERY_N_LINES

    def start(self):

        #self.sock.sendall('{} OpenAI: has joined the chat. say Hi!'.format(MessageProtocol.SYS_MSG).encode('ascii'))

        #message = self.sock.recv(1024).decode('ascii')


        return

    def changeTypeOfService(type: Enum):
        if type is TypeOfService.EVERY_N_SECS:
            typeOfService = TypeOfService.EVERY_N_SECS

        else:
            typeOfService = TypeOfService.EVERY_N_LINES


def main(host, port):
    # initialize and run GUI application

    client = Client(host, port)
    receive = client.start()

    aIClient = AIClient(host, port)
    aIClient.start()

    window = tk.Tk()
    window.title("Chatroom")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Text(master=fromMessage, yscrollcommand=scrollBar.set, state='disabled', height=10, width=30)
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

    selected_option = tk.StringVar(value="N lines")
    radButLine = tk.Radiobutton(window, text="AI Respond every N lines", value="N lines",
                   variable=selected_option, command=lambda :callingForChangesTypeOfService(TypeOfService.EVERY_N_LINES))

    radButSec = tk.Radiobutton(window, text="AI Respond every N secs", value="N secs",
                    variable=selected_option, command=lambda :callingForChangesTypeOfService(TypeOfService.EVERY_N_SECS))

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, pady=10, sticky="ew")
    radButLine.grid(row=2, column=0, padx=10, sticky="ew")
    radButSec.grid(row=2, column=1, padx=20, sticky="ew")

    def callingForChangesTypeOfService(type):
        #Tell aIClient to change The Type of service

        aIClient.changeTypeOfService(type)
        #Broadcast about the change radioButton to the clients

        #client.changeRadioMark(type)
        return



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