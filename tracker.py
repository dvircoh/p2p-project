import socket
import struct
import tracker_request_handler



HEADER_UNPACKING = '<I B I' # peer_id, message_code, payload_size
REQUEST_CODES = {'ADD_USER':0, 'REMOVE_USER':1, 'SEND_FILES_LIST':2, 'ADD_FILE':3, 'REMOVE_FILE':4}

def run_tracker(port):
    # Init socket
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.bind(("0.0.0.0", 12345))
    tracker_socket.listen()
    print("Tracker is up and running")
    data = ""
    while True:
        (peer_socket, peer_address) = tracker_socket.accept()
        print("Peer connected")
        read(peer_socket) # TODO :change read() to other name

def read(peer_socket):
    try:
        data_header = peer_socket.recv(struct.calcsize(HEADER_UNPACKING))
        peer_id, message_code, payloadsize = struct.unpack(HEADER_UNPACKING, data_header)
        if payload > 0: # For add_user and remove_user the payload empty
                    payload = peer_socket.recv(payloadsize)
        if message_code == REQUEST_CODES[REQUEST_CODES.ADD_USER]:
            tracker_request_handler.add_user_handler(peer_socket.address)
        elif message_code == REQUEST_CODES[REQUEST_CODES.REMOVE_USER]:
            tracker_request_handler.remove_user_handler(peer_id)
        elif message_code == REQUEST_CODES[REQUEST_CODES.SEND_FILES_LIST]:
            for message in tracker_request_handler.send_files_handler(payload):
                peer_socket.sendall(message)
        elif message_code == REQUEST_CODES[REQUEST_CODES.ADD_FILE]:
            tracker_request_handler.add_file_handler(peer_id)
        elif message_code == REQUEST_CODES[REQUEST_CODES.REMOVE_FILE]:
            tracker_request_handler.remove_file_handler(peer_id, payload)
        else:
            for message in tracker_request_handler.error():
                peer_socket.sendall(message)
        tracker_request_handler.update_last_connection_time(peer_id)
    # When/if user suddenly exits
    except ConnectionError:
        print("error with connection")
        peer_socket.close()
    # if exception happened receive error message
    except:
        for message in tracker_request_handler.error():
            peer_socket.sendall(message)


def main():
    print('''Hello and welcome to our P2P application!
You are our tracker!!!''')
    port = 12345
    run_tracker(port)


if __name__ == '__main__':
    main()
