import selectors
import socket
import struct
from enum import Enum
import peer_request_hendler

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER_UNPACKING = '<I B I' # client_id, message_code, payload_size
REQUEST_CODES = Enum('request', ['CONNECT', 'DISCONNECT', 'USERS_LIST', 'ADD_FILE','REQUEST_FILE'])

def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')
    ip = input("Please enter IP of tracker")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 12345))
    sock.send("hello world".encode())



def read(conn, mask):
        data_header = conn.recv(struct.calcsize(HEADER_UNPACKING))
        client_id, code, payloadsize = struct.unpack(HEADER_UNPACKING, data_header)
        payload = conn.recv(payloadsize)
        if code == REQUEST_CODES['CONNECT_REQUEST']:
            for message in connect_handler(payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["USERS_LIST"]:
            for message in users_list_handler(client_id, payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["ADD_FILE"]:  # get decrypted file, encrypt it and send CRC
            for message in self.requestHandler.encrypted_file_handler(payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["REQUEST_FILE"]:
            for message in self.requestHandler.valid_crc(payload):
                conn.sendall(message)
        else:
            for message in self.requestHandler.error():
                conn.sendall(message)
        self.requestHandler.update_last_connection_time(client_id)

if __name__ == '__main__':
    main()
