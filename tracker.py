import socket
import struct
import tracker_request_handler

HEADER_PACKING = '<I I' # message_code, payload_size
REQUEST_CODES = {'ADD_USER':0, 'ADD_FILE':1, 'REMOVE_FILE':2, 'GET_FILE':3, 'REMOVE_USER':4, 'SEND_FILES_LIST':5}

def run_tracker(port):
    # Init socket
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.bind(("0.0.0.0", 12345))
    tracker_socket.listen()
    print("Tracker is up and running")
    data = ""
    while True:
        try:
            (peer_socket,(peer_address, peer_port)) = tracker_socket.accept()
            print("Peer connected")
            read(peer_socket, peer_address) # TODO :change read() to other name
            peer_socket.close()
            # When/if user suddenly exits
        except ConnectionError:
            print("error with connection")
            peer_socket.close()
        # if exception happened receive error message
        except:
            print("error")


def read(peer_socket, peer_address):
        data_header = peer_socket.recv(struct.calcsize(HEADER_PACKING))
        message_code, payloadsize = struct.unpack(HEADER_PACKING, data_header)
        if payloadsize > 0: # For add_user and remove_user the payload empty
                    payload = peer_socket.recv(payloadsize)
        if message_code == REQUEST_CODES["ADD_USER"]:
            tracker_request_handler.add_user_handler(peer_address)
        elif message_code == REQUEST_CODES["REMOVE_USER"]:
            tracker_request_handler.remove_user_handler(peer_address)
        elif message_code == REQUEST_CODES["SEND_FILES_LIST"]:
            peer_socket.sendall(tracker_request_handler.send_files_handler())
        elif message_code == REQUEST_CODES["ADD_FILE"]:
            tracker_request_handler.add_file_handler(payload)
        elif message_code == REQUEST_CODES["REMOVE_FILE"]:
            tracker_request_handler.remove_file_handler(peer_address, payload)
        else:
            for message in tracker_request_handler.error():
                peer_socket.sendall(message)



def main():
    print('''Hello and welcome to our P2P application!
You are our tracker!!!''')
    port = 12345
    run_tracker(port)


if __name__ == '__main__':
    main()