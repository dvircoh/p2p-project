import struct

REQUEST_CODES = {'ADD_USER':        0, 
                 'ADD_FILE':        1, 
                 'REMOVE_FILE':     2, 
                 'GET_FILE':        3, 
                 'REMOVE_USER':     4,
                 'SEND_FILES_LIST': 5, 
                 'REQUEST_FILE':    6, 
                 'SEND_FILE':       7}

HEADER_PACKING =       '<I I' # message_code, payload_size
ADD_FILE_PACKING =     '<255s I' # file_name, checksum
REMOVE_FILE_PACKING =  '<255s' # file_name
REQUEST_FILE_PACKING = '<255s I' # file_name, chank_number
SEND_FILE_PACKING =    '<4096s I I' # data, actual size, checksum

# Generic function to create response header struct
def header_struct_generator(message_code, payload_size):
    return struct.pack(HEADER_PACKING, message_code, payload_size)