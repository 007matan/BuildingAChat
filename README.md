# Python Chat System 💻



## Overview 📜

The Python Chat System project is an educational endeavor designed to showcase the development of a networked chat application using Python.
It allows for real-time communication between multiple clients through a central server, emphasizing the practical application of networking concepts,
concurrency, and protocol design in Python.

![image](https://github.com/007matan/BuildingAChat/assets/25869697/4ec7e9ef-ba13-44ff-bed0-bfdcd8a87a52)




## Project Structure 🏗️


## Server 🖥️

The server component is designed to manage multiple client connections simultaneously, leveraging non-blocking sockets and select.select() for efficient handling.
It's responsible for receiving messages from one client and broadcasting them to all others, ensuring fluid communication across the network.

## Client 💻

The client component enables users to connect to the server, send messages, and receive broadcasts from other clients.
It showcases concurrent message sending and receiving, facilitated by threading to ensure that communication remains responsive and real-time.

## Message Protocol 📩

A simple, yet effective message protocol is implemented to standardize communication between clients and server.
Messages begin with a fixed-length header that denotes the size of the ensuing message, ensuring that message boundaries are respected and data integrity is maintained.

## Tests 🧪

Unit tests are included to validate the functionality of the server, client, and message protocol components.
These tests are crucial for ensuring reliability and stability of the chat system under various scenarios.


## Technologies Used 🛠️

Python: The core language used for the project, renowned for its simplicity and powerful standard library.
Socket Programming: For creating network connections between the server and clients.
Threading: To enable concurrent operations within the client for simultaneous sending and receiving of messages.
select.select(): Utilized by the server for non-blocking I/O operations, allowing it to handle multiple client connections efficiently.


## Usage 🚀

To use the Buildin A Chat App, follow these steps:
1. Clone the repository to your local machine.
2. Open the project on pycharm.
3. Server Connection: Open the terminal and run the command: python server.py localhost 
4. Client Connection: Open a new terminal or command prompt window, navigate to the project directory,
5.  and run python client.py 127.0.0.1 to connect a client to the server.
Engage in Chat: Repeat step 4 for connecting multiple clients and start chatting!


## File Descriptions 🗂️


# 'server.py'

The heart of the chat system, server.py, manages client connections, orchestrates message broadcasting,
and ensures seamless communication across all active clients. It uses non-blocking sockets and the select module for efficient network I/O,
handling multiple concurrent client connections without compromising performance.
# Development Time: 3 hours


# 'client.py' 

client.py acts as the interface for users to connect to the chat server, send messages, and receive updates from other participants.
It employs threading to manage simultaneous reading and writing operations, allowing users to engage in lively, uninterrupted chat sessions.
# Development Time: 2 hours


# messageProtocol.py 

This module defines the messaging protocol, including message formatting, encoding, and parsing logic.
It ensures that messages are correctly framed with a fixed-length header specifying the message length, facilitating accurate message transmission and reception.
# Development Time: 30 minutes


# tests.py 

The tests.py file contains unit tests for the server, client, and message protocol functionalities.
These tests are crucial for verifying the system's reliability and correctness under various conditions, providing a safety net for further development and refactoring.
# Development Time: 30 minutes


## Final Note 📝

As part of the work I was required to create an AI Client. The AI client will connect to the server and respond to the chat.
Unfortunately, after many hours I did not succeed in realizing this part of the project. I will continue in my spare time to learn more about ai api integration
And in general about fullstack applications in Python, so that I can finish this project as required.

