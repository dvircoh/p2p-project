import struct
from crc import crc32
import os

REQUEST_CODES = {'ADD_USER':0, 'ADD_FILE':1, 'REMOVE_FILE':2, 'GET_FILE':3, 'REMOVE_USER':4, 'SEND_FILES_LIST':5}
HEADER_PACKING = '<I I' # message_code, payload_size
ADD_FILE_PACKING = '<255s I'
REMOVE_FILE_PACKING = '<255s'
files = {}

def create_message(message_code, payload_size):
    return struct.pack(HEADER_PACKING, message_code, payload_size)

def crc_cksum(file_content):
    crc = crc32()
    crc.update(file_content)
    crc_checksum = crc.digest()
    return crc_checksum

def add_file_handler(file_path):
    file_name = os.path.basename(file_path)

    if file_name in files:
        print(files)
        print("file exist in the list")
        return [False]
    
    # Add file to list "files"
    files[file_name] = file_path
    try:
        file = open(file_path) # TODO check errors
        print("file opened succesfully " + file_name)
        checksum = crc_cksum(file.read().encode())
    except Exception as e:
        print(e)
        return [False]



    # Format: header(int request_code, int payload_size), message(string[255] file_name, int
    # checksum)
    return [create_message(REQUEST_CODES["ADD_FILE"], struct.calcsize(ADD_FILE_PACKING)),
     struct.pack(ADD_FILE_PACKING, file_name.encode(), checksum)]


def remove_file_handler(file_name):
    if file_name in files:
        # remove the file from the files dictionary
        del files[file_name]
        return [create_message(REQUEST_CODES["REMOVE_FILE"], struct.calcsize(REMOVE_FILE_PACKING)),
         struct.pack(REMOVE_FILE_PACKING, file_name.encode())]
    else:
        print("file does not exist in the list")
        return [False]

def remove_user_handler():
    return [create_message(REQUEST_CODES["REMOVE_USER"], 0)]

def send_files_list_handler():
    return [create_message(REQUEST_CODES["SEND_FILES_LIST"], 0)]


# # Generic function to create response header struct
# def header_struct_generator(code, payload_size):
#     return struct.pack('<B H L', SERVER_VERSION, code, payload_size)


# # For clients list creates struct for each client
# def client_struct_generator(client_id, client_name):
#     return struct.pack('<16s 255s', client_id, client_name)


# class RequestHandler:
#     def __init__(self):
#         self.users = [] #TODO set - list
#         self.files = []

#         name, public_key = struct.unpack('<255s 160s', payload)
#         # Strips null terminting values if there are
#         name = name.decode("utf-8").rstrip('\x00')
#         # returns error if name already exists in db (in Protocol should be uniqe)
#         if self.db.get_id_by_name(name):
#             self.error()
#         else:

#     def remove_user_handler(self, user_id):
#         client_list = self.db.get_clients_list(user_id)
#         message = [header_struct_generator(RESPONSE_CODE["client_list"], (UUID_SIZE + NAME_SIZE) * len(client_list))]
#         for client in client_list:
#             message.append(client_struct_generator(client[0], client[1]))
#         return message

#     def send_files_handler(self, payload):
#         client_id = struct.unpack('<16s', payload)[0]
#         return [header_struct_generator(RESPONSE_CODE["public_key"], UUID_SIZE + PUBLIC_KEY_SIZE),
#                 struct.pack('<16s 160s', client_id, self.db.get_public_key_by_id(client_id))]

#     def add_file_handler(self, user_id):
#         message_list = self.db.get_messages_by_id(user_id)
#         full_message = b''
#         for msg in message_list:
#             client_id, message_id, message_type, content = msg[0], msg[1], msg[2], msg[3]
#             full_message += struct.pack(f'<16s I B I {len(content)}s', client_id, int(message_id), message_type,
#                                         len(content), content)
#         return [header_struct_generator(RESPONSE_CODE["receive_messages"], len(full_message)), full_message]

#     def remove_file_handler(self, from_client_id, payload):
#         to_client_id, message_type, content_size = struct.unpack_from('<16s B I', payload)
#         # Reads message from char in place 21 after reading struct
#         message = payload[21:]
#         message_id = self.db.save_message(to_client_id, from_client_id, message_type, message)
#         return [header_struct_generator(RESPONSE_CODE["message_sent"], UUID_SIZE + MESSAGE_ID_SIZE),
#                 struct.pack('<16s I', to_client_id, message_id)]

#     # Error responed (9000) if error eccured
#     def error(self):
#         return [header_struct_generator(RESPONSE_CODE["internal_error"], NO_PAYLOAD)]
