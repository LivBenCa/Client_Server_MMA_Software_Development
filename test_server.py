import unittest
import pickle
from server import handle_data


class TestServer(unittest.TestCase):

    def test_handle_data_binary_dict(self):
        # Test handling of a BINARY dictionary
        binary_data = pickle.dumps({'key1': 'value1', 'key2': 'value2'})
        data_info = "SEND_D|B"
        result = handle_data(binary_data, data_info)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_handle_data_json_dict(self):
        # Test handling of a JSON dictionary
        json_data = '{"key1": "value1", "key2": "value2"}'
        data_info = "SEND_D|J"
        result = handle_data(json_data, data_info)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_handle_data_xml_dict(self):
        # Test handling of an XML dictionary
        xml_data = '<root><key1>value1</key1><key2>value2</key2></root>'
        data_info = "SEND_D|X"
        result = handle_data(xml_data, data_info)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_handle_data_encrypted_file(self):
        # Test handling of an encrypted file
        encrypted_data = b'\x10\x02\x03\x04'  # Example encrypted data
        data_info = "SEND_F|T"
        result = handle_data(encrypted_data, data_info)
        self.assertIsInstance(result, str)  # Assuming decrypted data is a string

    def test_handle_data_unencrypted_file(self):
        # Test handling of an unencrypted file
        unencrypted_data = b'This is unencrypted data'
        data_info = "SEND_F|F"
        result = handle_data(unencrypted_data, data_info)
        self.assertIsInstance(result, str)  # Assuming file data is a string


if __name__ == "__main__":
    unittest.main()
