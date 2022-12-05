import struct
import uuid

SERVER_VERSION = 2
UUID_SIZE = 16
PUBLIC_KEY_SIZE = 160
NAME_SIZE = 255
MESSAGE_ID_SIZE = 4
NO_PAYLOAD = 0

# Generic function to create response header struct
def header_struct_generator(code, payload_size):
    return struct.pack('<B H L', SERVER_VERSION, code, payload_size)


# For clients list creates struct for each client
def client_struct_generator(client_id, client_name):
    return struct.pack('<16s 255s', client_id, client_name)

def add_user_handler(address):
    print("add user. IP:" + address)
    


# def remove_user_handler(self, user_id):


# def send_files_handler(self, payload):


# def add_file_handler():


# def remove_file_handler():


# # Error responed (9000) if error eccured
# def error(self):
#     return [header_struct_generator(RESPONSE_CODE["internal_error"], NO_PAYLOAD)]
