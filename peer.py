import selectors
import socket
import struct
import peer_request_hendler

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tracker_ip = ""
REQUEST_CODES = {'ADD_USER':0, 'ADD_FILE':1, 'REMOVE_FILE':2, 'GET_FILE':3, 'REMOVE_USER':4, 'SEND_FILES_LIST':5}
HEADER_PACKING = '<I I' # message_code, payload_size

def create_messege(message_code, payload_size):
    return struct.pack(HEADER_PACKING, message_code, payload_size)

# Joining the network by sending a message to the tracker
def init():
    tracker_ip = input("Please enter IP of tracker")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tracker_ip, 12345))
    messege = create_messege(REQUEST_CODES["ADD_USER"], 0)
    sock.send(messege)
    sock.close()
    print("The connection was made successfully")    

# Returns the user's choice of the action they want to perform
def menu(): # TODO: check input
    choice = input('''What do you want do? (enter number)
    1. Add file
    2. Remove file
    3. Get file
    4. Disconnecting from the network
    ''')
    return choice

def actions(choice):
    if(choice == REQUEST_CODES['ADD_FILE']):
        peer_request_hendler.add_file_handler()
    #TODO: elif for 2-3-4

def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')
    init()
    while True:
        choice = menu()
        actions(choice)




def read(sock):
        data_header = sock.recv(struct.calcsize(HEADER_PACKING))
        code, payloadsize = struct.unpack(HEADER_PACKING, data_header)
        payload = sock.recv(payloadsize)
        if code == REQUEST_CODES["USERS_LIST"]:
            sock.sendall(peer_request_hendler.users_list_handler())
        elif code == REQUEST_CODES["ADD_FILE"]:  # get decrypted file, encrypt it and send CRC
            for message in peer_request_hendler.add_file_handler(payload):
                sock.sendall(message)
        elif code == REQUEST_CODES["REQUEST_FILE"]:
            for message in peer_request_hendler.valid_crc(payload):
                sock.sendall(message)
        else:
            for message in peer_request_hendler.error():
                sock.sendall(message)
        peer_request_hendler.update_last_sockection_time(client_id)

if __name__ == '__main__':
    main()
