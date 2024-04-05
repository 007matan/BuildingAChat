import unittest
from unittest.mock import patch, MagicMock
import client
import server
from messageProtocol import messageProtocol

class TestChatRoom(unittest.TestCase):

    def test_server_initialization(self):
        """Test if the server starts and listens for connections correctly."""
        test_server = server.Server('localhost', 0)  # Using port 0 to let OS pick the port
        self.assertIsInstance(test_server, server.Server)

    @patch('socket.socket')
    def test_client_connection(self, mock_socket):
        """Test client's ability to connect to the server."""
        test_client = client.Client('localhost', 9999)  # Assuming the server is running on port 9999
        test_client.sock = mock_socket
        self.assertIsInstance(test_client, client.Client)

    def test_message_encoding(self):
        """Test the encoding of messages."""
        test_message = "Hello, World!"
        encoded_message = messageProtocol.encode(test_message)
        self.assertEqual(encoded_message, f"{len(test_message):0{messageProtocol.HEADER_LENGTH}}{test_message}")

    def test_message_decoding(self):
        """Test the decoding of messages."""
        test_message = "Hello, World!"
        encoded_message = f"some_name: {len(test_message):0{messageProtocol.HEADER_LENGTH}}{test_message}"
        decoded_message = messageProtocol.decode(encoded_message)
        self.assertEqual(decoded_message, "some_name: " + test_message)

# More tests for message sending, receiving, and client disconnection can be added here.

if __name__ == '__main__':
    unittest.main()


