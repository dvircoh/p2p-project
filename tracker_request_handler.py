import struct
from utils import *

users = []
files = [] # name, checksum, size, list of ip addresses

def add_user_handler(ip_addr):
   # if ip_addr in users:
   #     print("user is already exist,try a different request")
   #     return False
    users.append(ip_addr)
    print(ip_addr)
    return True

def remove_user_handler(ip_addr):
    try:
        users.remove(ip_addr)
    except:
        print("can't remove user, maybe user is not exist")
        return False
    for file in files[:]:
       if ip_addr in file[3]:
           file[3].remove(ip_addr)
           if not file[3]:
               files.remove(file)
    return True


def add_file_handler(ip_addr, payload):
    file_name, checksum, file_size = struct.unpack(ADD_FILE_PACKING, payload)
    for file in files:
        if file_name == file[0]: # if file name already exist
            if checksum == file[1]: # identical checksum
                #TODO: don't add ip again if it exist
                file[3].append(ip_addr)
                return True
            return False
    # file name does not exist
    new_file_list = [file_name, checksum, file_size, [ip_addr]]
    print("new file list success")
    files.append(new_file_list)
    return True


def remove_file_handler(ip_addr,payload):
    file_name = struct.unpack('<255s', payload)[0]
    for file in files:
        if file_name == file[0]: #the file name
            #loop in order to find the ip address to extract from ip's list
            for ip in file[3]:
                if ip_addr == ip:
                    file[3].remove(ip)
                    if file[3] == []:
                        files.remove(file)
                    return True
    print("file does not exist")
    return False


def send_files_handler():
    files_string = str(files)
    files_string = files_string.encode('utf-8')
    print(files_string)
    list_length = len(files_string)
    print(type(files_string))
    return [header_struct_generator(REQUEST_CODES["SEND_FILES_LIST"], list_length),
     struct.pack(f'<{list_length}s',files_string)]
    
