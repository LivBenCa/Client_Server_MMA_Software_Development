import unittest
import pickle
from client import send_dictionary, send_file


class TestClient(unittest.TestCase):

    def test_send_dictionary(self):
        # Create a mock socket object (use a testing library like `unittest.mock` if available)
        class MockSocket:
            def __init__(self):
                self.sent_data = []

            def send(self, data):
                self.sent_data.append(data)

        mock_socket = MockSocket()
        dictionary = {'key1': 'value1', 'key2': 'value2'}
        data_format = "B"

        send_dictionary(mock_socket, dictionary, data_format)

        # Assert that the correct data was sent to the mock socket
        self.assertEqual(len(mock_socket.sent_data), 3)  # Three data pieces sent
        self.assertEqual(mock_socket.sent_data[0], str(len(pickle.dumps(dictionary))).encode())
        self.assertEqual(mock_socket.sent_data[1], f"SEND_D|{data_format}".encode())

    def test_send_file(self):
        # Create a mock socket object (use a testing library like `unittest.mock` if available)
        class MockSocket:
            def __init__(self):
                self.sent_data = []

            def send(self, data):
                self.sent_data.append(data)

        mock_socket = MockSocket()
        file_path = "test_file.txt"
        encrypt = "T"

        send_file(mock_socket, file_path, encrypt)

        # Implement similar assertions as in test_send_dictionary to check if the correct data was sent
        # You'll need to mock the file reading and encryption steps if necessary


if __name__ == "__main__":
    unittest.main()
