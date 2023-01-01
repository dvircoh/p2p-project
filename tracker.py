import socket
import struct
import tracker_request_handler
from utils import *


def run_tracker(port):
    # Init socket
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.bind(("0.0.0.0", port))
    tracker_socket.listen()
    print_tracker_is_on()

    # Main loop
    while True:
        try:
            (peer_socket,(peer_address, peer_port)) = tracker_socket.accept()
            print("Peer connected")
            recieve_from_peers(peer_socket, peer_address)
            peer_socket.close()
            # When/if user suddenly exits
        except ConnectionError:
            print("error with connection")
            peer_socket.close()
        # if exception happened receive error message
        except Exception as e:
            print(e)


def recieve_from_peers(peer_socket, peer_address):
        data_header = peer_socket.recv(struct.calcsize(HEADER_PACKING))
        message_code, payload_size = struct.unpack(HEADER_PACKING, data_header)

        if payload_size > 0: # For add_user and remove_user the payload empty
                    payload = peer_socket.recv(payload_size)

        if message_code == REQUEST_CODES["ADD_USER"]:
            success = tracker_request_handler.add_user_handler(peer_address)
            peer_socket.send(str(success).encode())

        elif message_code == REQUEST_CODES["REMOVE_USER"]:
            success = tracker_request_handler.remove_user_handler(peer_address)
            peer_socket.send(str(success).encode())

        elif message_code == REQUEST_CODES["SEND_FILES_LIST"]:
            files_list = tracker_request_handler.send_files_handler()
            peer_socket.sendall(files_list[0])
            peer_socket.sendall(files_list[1])

        elif message_code == REQUEST_CODES["ADD_FILE"]:
            success = tracker_request_handler.add_file_handler(peer_address, payload)
            peer_socket.send(str(success).encode())

        elif message_code == REQUEST_CODES["REMOVE_FILE"]:
            success = tracker_request_handler.remove_file_handler(peer_address, payload)
            peer_socket.send(str(success).encode())


        else:
            for message in tracker_request_handler.error():
                peer_socket.sendall(message)


def print_tracker_is_on():

    print(''' _______          ______         _______  
|       \        /      \       |       \ 
| $$$$$$$\      |  $$$$$$\      | $$$$$$$\ 
| $$__/ $$       \$$__| $$      | $$__/ $$
| $$    $$       /      $$      | $$    $$
| $$$$$$$       |  $$$$$$       | $$$$$$$ 
| $$            | $$_____       | $$      
| $$            | $$     \      | $$      
 \$$             \$$$$$$$$       \$$  
              ''')

    print("Tracker is up and running")
    data = ""
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("--------------------------------------")
    print("| Tracker IP Address is:  " + IPAddr+"    |")
    print("--------------------------------------")


def main():
    print('''Hello and welcome to our P2P application!
You are our tracker!!!''')
    port = 12345
    run_tracker(port)


if __name__ == '__main__':
    main()
