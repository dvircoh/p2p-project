import selectors
import socket
import struct
import peer_request_handler

def send_to_tracker(tracker_ip, message):
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.connect((tracker_ip, 12345))
    for item in message:
        tracker_socket.sendall(item)
    success = bool(tracker_socket.recv(1).decode())
    tracker_socket.close()
    return success

# Joining the network by sending a message to the tracker
def init(tracker_ip):
    # Create "message" as list for consistenty in send_to_tracker()
    message = [peer_request_handler.create_message(peer_request_handler.REQUEST_CODES["ADD_USER"], 0)]
    success = send_to_tracker(tracker_ip, message)
    return success  

# Returns the user's choice of the action they want to perform
def menu(): # TODO: check input
    choice = input('''What do you want to do? (enter number)
    1. Add file
    2. Remove file
    3. Get file
    4. Disconnecting from the network
    ''')
    return int(choice)

def actions(tracker_ip, choice):
    if(choice == peer_request_handler.REQUEST_CODES['ADD_FILE']):
        file_path = input("enter file path for adding:")
        message = peer_request_handler.add_file_handler(file_path)
        if message[0] == 0: # file adding failed
            return
        success = send_to_tracker(tracker_ip, message)
        if success:
            print("add file success")
        else:
            print("add file don't success, try again")
    elif(choice == peer_request_handler.REQUEST_CODES['REMOVE_FILE']):
        file_name = input("enter filename for remove:")
        message = peer_request_handler.remove_file_handler(file_name)
        success = send_to_tracker(tracker_ip, message)
        if success:
            print("remove file success")
        else:
            print("remove file don't success, try again")
    elif(choice == peer_request_handler.REQUEST_CODES['REMOVE_USER']):
        message = peer_request_handler.remove_user_handler()
        success = send_to_tracker(tracker_ip, message)
        if success:
            print("disconnecting success")
        else:
            print("disconnecting don't success")
    elif(choice == peer_request_handler.REQUEST_CODES['SEND_FILES_LIST']):
        message = peer_request_handler.send_files_list_handler()
        success = send_to_tracker(tracker_ip, message)
        if success:
            # receive list
            print("")
        else:
            print("")

def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')
    init_success = False

    # Loop for join tracker lists
    while not init_success:
        tracker_ip = input("Please enter IP of tracker")
        init_success = init(tracker_ip)
        if init_success:
            print("The connection was made successfully")
        else:
            print("The connection failed try again")
    
    # Tha main loop
    while True:
        choice = menu()
        actions(tracker_ip, choice)

def read(sock):
        data_header = sock.recv(struct.calcsize(HEADER_PACKING))
        code, payloadsize = struct.unpack(HEADER_PACKING, data_header)
        payload = sock.recv(payloadsize)
        if code == peer_request_handler.REQUEST_CODES["USERS_LIST"]:
            sock.sendall(peer_request_handler.users_list_handler())
        elif code == peer_request_handler.REQUEST_CODES["ADD_FILE"]:  # get decrypted file, encrypt it and send CRC
            file_name, checksum = peer_request_handler.add_file_handler(payload)

            sock.sendall(message)
        elif code == peer_request_handler.REQUEST_CODES["REQUEST_FILE"]:
            for message in peer_request_handler.valid_crc(payload):
                sock.sendall(message)
        else:
            for message in peer_request_handler.error():
                sock.sendall(message)
        peer_request_handler.update_last_sockection_time(client_id)

if __name__ == '__main__':
    main()
