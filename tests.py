import unittest
from unittest.mock import patch, MagicMock
import client
import server
from MessageProtocol import MessageProtocol


class TestChatRoom(unittest.TestCase):

    def testServerInitialization(self):
        """Test if the server starts and listens for connections correctly."""
        test_server = server.Server('localhost', 0)  # Using port 0 to let OS pick the port
        self.assertIsInstance(test_server, server.Server)

    @patch('socket.socket')
    def testClientConnection(self, mock_socket):
        """Test client's ability to connect to the server."""
        test_client = client.Client('localhost', 9999)  # Assuming the server is running on port 9999
        test_client.sock = mock_socket
        self.assertIsInstance(test_client, client.Client)

    def testMessageEncoding(self):
        """Test the encoding of messages."""
        test_message = "Hello, World!"
        encoded_message = MessageProtocol.encode(test_message)
        self.assertEqual(encoded_message, f"{len(test_message):0{MessageProtocol.HEADER_LENGTH}}{test_message}")

    def testMessageDecoding(self):
        """Test the decoding of messages."""
        test_message = "Hello, World!"
        encoded_message = f"some_name: {len(test_message):0{MessageProtocol.HEADER_LENGTH}}{test_message}"
        decoded_message = MessageProtocol.decode(encoded_message)
        self.assertEqual(decoded_message, "some_name: " + test_message)



# More tests for message sending, receiving, and client disconnection can be added here.


if __name__ == '__main__':
    unittest.main()


