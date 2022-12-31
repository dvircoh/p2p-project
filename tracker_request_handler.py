import struct
from utils import *

users = [] # ip address
files = [] # name, checksum, size, list of ip addresses

def add_user_handler(ip_addr: str):
    if ip_addr not in users:
        users.append(ip_addr)
    print(ip_addr + "connect to the network")
    return True

def remove_user_handler(ip_addr):
    try:
        users.remove(ip_addr)
    except:
        print("can't remove user, maybe user does not exist")
        return False
    
    # Remove user from the files he added, if have not more peers added this file remove file.
    for file in files[:]:
       if ip_addr in file[3]:
           file[3].remove(ip_addr)
           if not file[3]:
               files.remove(file)
    print(ip_addr + "remove from the network")
    return True


def add_file_handler(ip_addr, payload):
    file_name, checksum, file_size = struct.unpack(ADD_FILE_PACKING, payload)

    for file in files:
        if file_name == file[0]: # if file name already exist
            if checksum == file[1]: # identical checksum
                if ip_addr not in file[3]:
                    file[3].append(ip_addr)
                    return True
            print("There is already file with this name but with different content. please rename your file and try to add it again")
            return False # Checksum unmatch or user already exist in the list
    # File name does not exist so add new file to files list
    new_file = [file_name, checksum, file_size, [ip_addr]]
    print("add new file to list success")
    files.append(new_file)
    return True


def remove_file_handler(ip_addr,payload):
    file_name = struct.unpack('<255s', payload)[0]
    for file in files:
        if file_name == file[0]: #the file name
            #loop in order to find the ip address to extract from ip's list
            for ip in file[3]:
                if ip_addr == ip:
                    file[3].remove(ip)
                    if not file[3]:
                        files.remove(file)
                    return True
    print("file does not exist")
    return False


def send_files_handler():
    files_string = str(files).encode('utf-8')
    list_length = len(files_string)
    return [header_struct_generator(REQUEST_CODES["SEND_FILES_LIST"], list_length),
     struct.pack(f'<{list_length}s',files_string)]


    