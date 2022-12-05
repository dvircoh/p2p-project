import selectors
import socket
import struct
import peer_request_hendler

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

REQUEST_CODES = {'ADD_USER':0, 'REMOVE_USER':1, 'SEND_FILES_LIST':2, 'ADD_FILE':3, 'REMOVE_FILE':4}
HEADER_PACKING = '<I I' # message_code, payload_size

def create_messege(message_code, payload_size):
    return struct.pack(HEADER_PACKING, message_code, payload_size)

def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')
    ip = input("Please enter IP of tracker")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 12345))
    messege = create_messege(REQUEST_CODES["ADD_USER"], 0)
    sock.send(messege)



def read(conn, mask):
        data_header = conn.recv(struct.calcsize(HEADER_PACKING))
        client_id, code, payloadsize = struct.unpack(HEADER_PACKING, data_header)
        payload = conn.recv(payloadsize)
        if code == REQUEST_CODES['CONNECT_REQUEST']:
            for message in connect_handler(payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["USERS_LIST"]:
            for message in users_list_handler(client_id, payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["ADD_FILE"]:  # get decrypted file, encrypt it and send CRC
            for message in peer_request_hendler.encrypted_file_handler(payload):
                conn.sendall(message)
        elif code == REQUEST_CODES["REQUEST_FILE"]:
            for message in peer_request_hendler.valid_crc(payload):
                conn.sendall(message)
        else:
            for message in peer_request_hendler.error():
                conn.sendall(message)
        peer_request_hendler.update_last_connection_time(client_id)

if __name__ == '__main__':
    main()
