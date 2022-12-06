import struct

# Generic function to create response header struct
def header_struct_generator(code, payload_size):
    return struct.pack('<I I', code, payload_size)

def add_user_handler(address):
    print("add user. IP:" + address)
    
def remove_user_handler(address):
    print("remove user. IP:" + address)


def send_files_handler():
    print("send files")
   

def add_file_handler(file):
    print("add file" + file)


def remove_file_handler(address, file):
    print("remove file" + file + address)
