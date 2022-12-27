import struct

REQUEST_CODES = {'ADD_USER':        0, 
                 'ADD_FILE':        1, 
                 'REMOVE_FILE':     2, 
                 'GET_FILE':        3, 
                 'REMOVE_USER':     4,
                 'SEND_FILES_LIST': 5, 
                 'REQUEST_FILE':    6, 
                 'SEND_FILE':       7}

CHUNK_SIZE = 4096

HEADER_PACKING          =       '<I I'           # message_code, payload_size
ADD_FILE_PACKING        =       '<255s I I'      # file_name, checksum, file_size
REMOVE_FILE_PACKING     =       '<255s'          # file_name
REQUEST_FILE_PACKING    =       '<255s I'        # file_name, chunk_number
SEND_FILE_PACKING       =       f'<{CHUNK_SIZE}s I I'     # data, actual size, checksum

# Generic function to create response header struct
def header_struct_generator(message_code, payload_size):
    return struct.pack(HEADER_PACKING, message_code, payload_size)
    