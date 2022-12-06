import struct
users = []
files = [] # name, checksum, list of ip addresses

# Generic function to create response header struct
def header_struct_generator(code, payload_size):
    return struct.pack('<I I', code, payload_size)

def add_user_handler(ip_addr):
    users.append(ip_addr)
    print(ip_addr)

def remove_user_handler(ip_addr):
    users.remove(ip_addr)

def add_file_handler(ip_addr,payload):
    file_name,checksum = struct.unpack('<255s I', payload)
    print(file_name.decode())
    print("checksum is" )
    print( checksum )
    for file in files:
        if file_name == file[0]: # if file name already exist
            print("im in file_name")
            if checksum == file[1]: # identical checksum

                file[2].append(ip_addr)
                return True
            return False
    # file name does not exist

    print("im in end of files")

    new_file_list = [file_name, checksum, [ip_addr]]
    print("new file list success")
    files.append(new_file_list)
    print("append")
    return True


def remove_user_handler(ip_addr):
    print("remove user")