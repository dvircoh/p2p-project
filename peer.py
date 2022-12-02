import selectors
import socket
import struct
from enum import Enum
import peer_request_hendler

sel = selectors.DefaultSelector()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER_UNPACKING = '<I B I' # client_id, message_code, payload_size
REQUEST_CODES = Enum('request', ['CONNECT', 'DISCONNECT', 'USERS_LIST', 'ADD_FILE','REQUEST_FILE'])

def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')
    ip = input("Please enter IP of tracker")
    sock.bind((ip, 12345))
    sock.listen(100)
    sel.register(sock, selectors.EVENT_READ, accept)
    run_server()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def run_server():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

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
