import threading
import socket
import argparse
import os
from messageProtocol import messageProtocol

"""
Class Server:
This class defines a server for a Chat Room Simulation.
    ...
    Constructor
    -------
    __init__(self, host, port)
    The constructor for the Server class. It initializes
    the connections list to an empty list, 
    and stored provided host name, and number of port.  
    ...
    Methods
    -------
    run(self)
        The function define thread logic by creating a socket.socket object,
        the socket take two argument: address and the socket type.
        AF_INET (address) for the ip networking, and the SOCK_STREAM
        (socket type) for the reliable flow control data stream.
        Next we use SO_REUSEADDR to actually allow the server to use
        the same port after an old connection was closed.
        After that we use the bind method to actually bind the socket
        object to the socket address on the server machine.
        bind method takes in a tuple in this format (ip address - string
        , port number - int). Then we use the listen method to indicate that
        this is a listening socket (and not connected socket)
        Finally the function accepting new connection, then creates
        a new thread, start the thread and add the thread to active connection.
        
    broadcast(self, message, source)
        The function get as parameters: the massage as char sequence
        , and the source client.the function send to all connected 
        client accept the source client.
     
    remove_connection(self, connection)
        The function get as parameter: the connection as Connection object.
        the function remove the connection from the connections.
    ...
    Functionality
    -------    
    This class Server, represents a threaded server that manages
    multiple client connections in a network.Here's the functionality
    of each part of the class. It's provides the core functionality
    for managing incoming connections, broadcasting messages to
    connected clients, and removing disconnected clients.
    It's designed to be used as part of a multi-threaded server application.
"""


class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print("Listening at", sock.getsockname())

        while True:
            sc, sockname = sock.accept()
            print(f"New connection from {sc.getpeername()} to {sc.getsockname()}")

            server_socket = ServerSocket(sc, sockname, self)

            server_socket.start()

            self.connections.append(server_socket)
            print("Ready to receive massage from", sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:

            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


"""
Class ServerSocket:
This Class will manage our thread creation.

    ...
    Constructor
    -------
    __init__(self, sc, sockname, server)
    The function get as parameter: socket connection between the 
    server and the client, address of the client's socket, parent
    Server object that manages this socket. The function init the
    class by the provided parameters (sc - connection socket
    , sockname - client socket address, server - parent thread)
    ...
    Methods
    -------
    run(self)
        We're going to receive a data from the connected client and
        broadcast that message to all other clients from the list of
        server socket thread in the parent server thread

    send(self, message)
        The function get as parameter: a char sequence as a massage
        The function send a message to the connected server.
        
    exit(server)
        The function get as parameter: server  - The Server object
        representing the chat server. This function runs in a loop,
        continually waiting for user input. If the user types 'q'
        followed by pressing Enter, it triggers the server shutdown.
        Upon receiving 'q', the function closes all active connections
        and shuts down the server.
    ...
    Functionality
    -------    
    the ServerSocket class is responsible for handling communication
    with individual clients. It receives messages from clients
    , broadcasts them to other clients, and manages the shutdown
    process when necessary.
    Error handling is implemented to handle unexpected events,
    such as connection errors or user termination.
"""


class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            try:
                message = self.sc.recv(1024).decode('ascii')
                if message:
                    print(f"{self.sockname} says {message}")
                    self.server.broadcast(messageProtocol.decode(message), self.sockname)
                else:
                    print(f"Connection with client {self.sockname} forcibly closed.")
                    self.sc.close()
                    self.server.remove_connection(self)
                    break
            except ConnectionResetError:
                print(f"Connection with client {self.sockname} forcibly closed.")
                self.sc.close()
                self.server.remove_connection(self)
                break

    def send(self, message):
        try:
            self.sc.sendall(message.encode('ascii'))
        except ConnectionResetError:
            print("Connection with client {} forcibly closed.".format(self.sockname))
            self.sc.close()
            self.server.remove_connection(self)

    def exit(server):
        while True:
            inpt = input("")
            if inpt == "q":
                print("Closing all connections...")
                for connection in server.connections:
                    connection.sc.close()

                print("Shutting down the server...")
                os.exit(0)


"""
This block serves as the entry point of the script when executed directly.
It creates an instance of the Server class with the provided host and port,
then starts the server thread. It starts a separate thread to handle the
server shutdown process. However, it seems there's an issue with the usage
of exit function as a target for the thread. It should be replaced with a
correct function or method that handles server shutdown.
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')

    args = parser.parse_args()

    # create and start server thread
    server = Server(args.host, args.p)
    server.start()

    exit = threading.Thread(target=exit, args = (server, ))
    exit.start()



