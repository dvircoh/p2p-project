import struct
from crc import crc32
import os
from utils import *

files = {}

# Return checksum of file. 
def crc_cksum(file_content: bytes)->int:
    crc = crc32()
    crc.update(file_content)
    crc_checksum = crc.digest()
    return crc_checksum

def add_file_handler(file_path: str)->list:
    file_path = file_path.strip()
    file_name = os.path.basename(file_path)
    file_size = 0

    if file_name in files:
        print(files)
        print("This file already exist in the list")
        return [False]
    
    try:
        file = open(file_path.strip()) # TODO check errors
        print("file opened succesfully " + file_name)
        checksum = crc_cksum(file.read().encode())
        # Add file to list "files"
        files[file_name] = file_path
        file_size = os.path.getsize(file_path)
        print("file size is:")
        print(file_size)
    except Exception as e:
        print(e)
        return [False]

    # Format: header(int request_code, int payload_size), message(string[255] file_name, int
    # checksum, int file_size)
    return [header_struct_generator(REQUEST_CODES["ADD_FILE"], struct.calcsize(ADD_FILE_PACKING)),
     struct.pack(ADD_FILE_PACKING, file_name.encode(), checksum, file_size)]


def remove_file_handler(file_name: str)->list:
    if file_name in files:
        # remove the file from the files dictionary
        del files[file_name]
        return [header_struct_generator(REQUEST_CODES["REMOVE_FILE"], struct.calcsize(REMOVE_FILE_PACKING)),
         struct.pack(REMOVE_FILE_PACKING, file_name.encode())]
    else:
        print("file does not exist in the list")
        return [False]

def remove_user_handler()->list:
    return [header_struct_generator(REQUEST_CODES["REMOVE_USER"], 0)]

def send_files_list_handler()->list:
    return [header_struct_generator(REQUEST_CODES["SEND_FILES_LIST"], 0)]
