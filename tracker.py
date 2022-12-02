import selectors
import socket
import struct
from enum import Enum
import tracker_request_handler



HEADER_UNPACKING = '<I B I' # client_id, message_code, payload_size
REQUEST_CODES = {'ADD_USER':0, 'REMOVE_USER':1, 'SEND_FILES_LIST':2, 'ADD_FILE':3, 'REMOVE_FILE':4}


class SelectorServer:
    def __init__(self, port):
        self.request_handler = tracker_request_handler()
        # Socket with Protocol IPv4, TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.soc:
            self.soc.bind(('', port))
            self.soc.listen(100)
            self.sel = selectors.DefaultSelector()
            self.sel.register(self.soc, selectors.EVENT_READ, self.accept)
            self.run_server()


    def accept(self, sock, mask):
        conn, addr = sock.accept()
        print(f'accepted {conn} from {addr}')
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        try:
            data_header = conn.recv(struct.calcsize(HEADER_UNPACKING))
            client_id, version, code, payloadsize = struct.unpack(HEADER_UNPACKING, data_header)
            payload = conn.recv(payloadsize)
            if code == REQUEST_CODES[REQUEST_CODES.ADD_USER]:
                self.request_handler.add_user_handler(payload)
            elif code == REQUEST_CODES[REQUEST_CODES.REMOVE_USER]:
                self.request_handler.remove_user_handler(client_id)
            elif code == REQUEST_CODES[REQUEST_CODES.SEND_FILES_LIST]:
                for message in self.request_handler.send_files_handler(payload):
                    conn.sendall(message)
            elif code == REQUEST_CODES[REQUEST_CODES.ADD_FILE]:
                self.request_handler.add_file_handler(client_id)
            elif code == REQUEST_CODES[REQUEST_CODES.REMOVE_FILE]:
                self.request_handler.remove_file_handler(client_id, payload)
            else:
                for message in self.request_handler.error():
                    conn.sendall(message)
            self.request_handler.update_last_connection_time(client_id)
        # When/if user suddenly exits
        except ConnectionError:
            print("error with connection")
            self.sel.unregister(conn)
            conn.close()
        # if exception happened receive error message
        except:
            for message in self.request_handler.error():
                conn.sendall(message)

    def run_server(self):
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


def main():
    print('''Hello and welcome to our P2P application!
You are our tracker!!!''')
    port = 12345
    SelectorServer(port)


if __name__ == '__main__':
    main()
