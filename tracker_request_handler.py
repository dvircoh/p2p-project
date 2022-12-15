import struct
users = []
files = [] # name, checksum, list of ip addresses
HEADER_PACKING = '<I I' # message_code, payload_size
REQUEST_CODES = {'ADD_USER':0, 'ADD_FILE':1, 'REMOVE_FILE':2, 'GET_FILE':3, 'REMOVE_USER':4, 'SEND_FILES_LIST':5}

# Generic function to create response header struct
def header_struct_generator(code, payload_size):
    return struct.pack(HEADER_PACKING, code, payload_size)

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

def add_file_handler(ip_addr, payload):
    file_name,checksum = struct.unpack('<255s I', payload)
    print(file_name.decode())
    print("checksum is" )
    print(checksum)
    for file in files:
        if file_name == file[0]: # if file name already exist
            if checksum == file[1]: # identical checksum
                file[2].append(ip_addr)
                return True
            return False
    # file name does not exist

    new_file_list = [file_name, checksum, [ip_addr]]
    print("new file list success")
    files.append(new_file_list)
    print("append")
    return True


def remove_file_handler(ip_addr,payload):
    file_name = struct.unpack('<255s', payload)[0]
    for file in files:
        if file_name == file[0]: #the file name
            #loop in order to find the ip address to extract from ip's list
            for ip in file[2]:
                if ip_addr == ip:
                    file[2].remove(ip)
                    return True
    print("file does not exist")
    return False


def send_files_handler():
    files_string = files.encode()
    list_length = len(files_string)
    return [header_struct_generator(REQUEST_CODES["SEND_FILES_LIST"], list_length),
     struct.pack('<{list_length}s', files_string)]
    
