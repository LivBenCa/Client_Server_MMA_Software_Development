import socket
import threading
import sys
import pickle
import json
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
import tqdm

# Define the server´s port and host information
PORT = 8080
HOST = ""
SERVER_ADDR = (HOST, PORT)
BUFFER = 1024

# Insert your own encryption key and nonce
KEY = b"YourOwnSecretKey"
NONCE = b"YourOwnSecretNce"

# create an INET, STREAMing socket to listen for incoming connections
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"[ERROR] Error creating socket: {e}")
    sys.exit(1)

try:
    # Bind the server socket to the specified address and port
    server_socket.bind(SERVER_ADDR)
except socket.error as e:
    print(f"[ERROR] Socket binding failed with error: {e}")
    sys.exit(1)


# Funtion to handle dictionaries sent in different formats
def handle_dict(data_format, serialized_dict):
    # Deserialize the dictionary sent in Binary format
    if data_format == "B":
        original_dict = pickle.loads(serialized_dict)
    # Deserialize the dictionary sent in JSON format
    elif data_format == "J":
        original_dict = json.loads(serialized_dict)
    # Deserialize the dictionary sent in XML format
    elif data_format == "X":
        root = ET.fromstring(serialized_dict)
        original_dict = {child.tag: child.text for child in root}
    else:
        raise ValueError("Received data is neither valid JSON, binary, nor XML.")

    # Print the dictionary to the screen
    print(f"[DICT_TO_SCREEN] Dictionary was sent in {data_format} format: {original_dict}")
    # Write the dictionary to a file
    with open("dict_to_file.txt", "w") as file:
        file.write(str(original_dict))


# Funtion to handle files sent with or without encryption
def handle_file(encryption, file_data):
    # Handle files without encryption
    if encryption == "F":
        decoded_file = file_data.decode()

        # Print to decoded file data to the screen
        print(f"[PRINT_TO_SCREEN] Content of the file: {decoded_file}")
        # Write the decoded file data into the file
        with open("file_server.txt", "w") as file:
            file.write(decoded_file)

    # Handle files with encryption
    elif encryption == "T":
        # Create and AES cipher object for decryption
        cipher = AES.new(KEY, AES.MODE_EAX, NONCE)
        # Decrypt the "file_dat" using the previously created AES cipher
        decrypt_data = cipher.decrypt(file_data).decode()

        # Print the decrypted file data to the screen
        print(f"[PRINT_TO_SCREEN] Content of the encrypted file: {decrypt_data}")
        # Write the decrypted filedata into the file
        with open("file_server.txt", "w") as dec_file:
            dec_file.write(decrypt_data)


# Function to handle received data based on the header and format
def handle_data(received_data, data_info):
    # Split the 'data_info' string using the "|" character as the delimiter
    split = data_info.split("|")
    # Extract the header and data format from the split "data_info"
    header = split[0]
    data_format = split[1]
    print(header, data_format, sep="\n")
    # Check if the 'header' is "SEND_D" (indicating a dictionary data type)
    if header == "SEND_D":
        handle_dict(data_format, received_data)
    # Check if the 'header' is "SEND_F" (indicating a file data type)
    elif header == "SEND_F":
        handle_file(data_format, received_data)


# Function to handle a connected client
def handle_client(client_socket, client_addr):
    print(f"[NEW CONNECTION] {client_addr} is connected to the server")

    # Receive and decode the size of sent data from the client
    data_size = int(client_socket.recv(BUFFER).decode())

    try:
        # Receive and decode information about the data format and type
        data_info = client_socket.recv(8).decode()
    except socket.error as msg:
        print(f"[ERROR] Error receiving data: {msg}")
        sys.exit(1)

    # Initialize an empty 'received_data' bytes object to store the received data
    received_data = b""

    # Create a progress bar using tqdm to track the data reception progress
    progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(data_size))

    # Continue receiving data from the client in chunks until the entire data is received
    while True:
        try:
            # Receive a chunk of data from the client (maximum size determined by BUFFER)
            chunk_of_data = client_socket.recv(BUFFER)
        except socket.error as msg:
            print(f"[ERROR] Error receiving data: {msg}")
            sys.exit(1)
        # Append the received chunk to the "received_data" bytes object
        received_data += chunk_of_data
        # Update the progress bar to reflect the amount of data received
        progress.update(BUFFER)
        # Exit the loop, if all data has been received
        if len(chunk_of_data) < BUFFER:
            break
    # Call the 'handle_data' function to process the received data
    handle_data(received_data, data_info)


# Function to start the sever and handle client connections
def start():
    try:
        # Listen for incoming connections
        server_socket.listen()
    except socket.error as msg:
        print(f"[ERROR] Socket listen failed with error: {msg}")
        sys.exit(1)

    while True:
        try:
            # Accept connection when a client connects
            client_socket, client_addr = server_socket.accept()
        except socket.error as msg:
            print(f"[ERROR] Error accepting connections from client: {msg}")
            sys.exit(1)
        # Create a thread to handle each client connection
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
