import asyncio
from math import ceil, floor
from utils import *
from peer_request_handler import *
import sys
import struct
import os

async def ainput(string: str) -> str:
    print(string + " ")
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

# Send message to tracker
# Return success status
async def send_to_tracker(tracker_ip: str, message: list)->bool:
    reader, writer = await asyncio.open_connection(tracker_ip, 12345)
    for item in message:
        writer.write(item)
        await writer.drain()
    success = bool(await reader.read(1))
    writer.close()
    await writer.wait_closed()
    return success

# Send message to tracker
# Return tracker answer
async def send_and_recv_tracker(tracker_ip: str, message: list)->bytes:
    reader, writer = await asyncio.open_connection(tracker_ip, 12345)

    for item in message:
        writer.write(item)
        await writer.drain()

    data_header = await reader.read(struct.calcsize(HEADER_PACKING))
    message_code, payload_size = struct.unpack(HEADER_PACKING, data_header)
    payload = await reader.read(payload_size)

    writer.close()
    await writer.wait_closed()
    return payload

# Joining the network by sending a message to the tracker
async def init(tracker_ip)->bool:
    # Create "message" as list for consistenty in send_to_tracker()
    message = [header_struct_generator(REQUEST_CODES["ADD_USER"], 0)]
    success = await send_to_tracker(tracker_ip, message)
    return success  

# Returns the user's choice of the action they want to perform
async def menu()->int:
    while True:
        try:
            choice = await ainput('''What do you want to do? (enter number)
            1. Add file
            2. Remove file
            3. Get file
            4. Disconnecting from the network
            ''')
            choice = int(choice.strip())
            if choice < 1 or choice > 4:
                print("Please enter number from the options")
            else:
                break
        except ValueError:
            print("Please enter only number")
    return choice

async def select_file(files_list: list)->int:
    print("Please select a file from the following files")

    for index, file in enumerate(files_list):
        # print index and file_name
        print(str(index) + ") - " + file[0].decode().rstrip('\x00'))

    while True:
        try:
            choice = await ainput("Enter the file number you want")
            choice = int(choice.strip())
            if choice < 0 or choice > len(files_list) - 1:
                print("Please enter number from the options")
            else:
                break
        except ValueError:
            print("Please enter only number")
    return choice

async def tracker_connection():
    init_success = False

    # Loop for join tracker lists
    while not init_success:
        try:
            tracker_ip = input('''
            Please enter IP of tracker -  ''')

            tracker_ip = tracker_ip.strip()
            init_success = await init(tracker_ip)
            if init_success:
                print_success_connection()
            else:
                print("The connection failed try again")
        except Exception as e:
            print('''
            The connection failed.
            try again and make sure that the tracker is running at first
            and that the ip address is correct\n''')

    choice = 0
    while choice != REQUEST_CODES['REMOVE_USER']:
        try:
            choice = await menu()
            await actions(tracker_ip, choice)
        except Exception as e:
            print(e)



async def actions(tracker_ip, choice):
    if(choice == REQUEST_CODES['ADD_FILE']):
        file_path = await ainput("enter file path for adding:")
        message = add_file_handler(file_path)
        if message[0] == 0: # file adding failed
            return
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("add file success")
        else:
            print("add file don't success, try again")

    elif(choice == REQUEST_CODES['REMOVE_FILE']):
        print("The files you added to the network are:")
        for index, file in enumerate(files):
            # print index and file_name
            print(str(index) + ") - " + file)
        file_name = await ainput("enter filename for remove:")
        message = remove_file_handler(file_name)
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("remove file success")
        else:
            print("remove file don't success, try again")

    elif(choice == REQUEST_CODES['REMOVE_USER']):
        message = remove_user_handler()
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("disconnecting success")
            print("bye bye")
        else:
            print("disconnecting don't success")

    elif(choice == REQUEST_CODES['GET_FILE']):
        message = send_files_list_handler()
        result = await send_and_recv_tracker(tracker_ip, message)

        # Create list from the bytes
        files_list = eval(result.decode('utf-8'))
        if files_list == []: # Check if the list empty
            print("The file list is empty, there are no files to receive")
        else:
            choice = await select_file(files_list)
            success = await receive_file(files_list[choice])
            if success:
                # Added new file to tracker
                file_name =  files_list[choice][0].decode().rstrip('\x00')
                new_file_path = os.path.join(os.getcwd(), 'P2P-Downloads', file_name)
                if file_name not in files:
                    message = add_file_handler(new_file_path)
                    await send_to_tracker(tracker_ip, message)

async def receive_file(file: list)->bool:
    peers_list = file[3]
    file_size = file[2]
    file_name = file[0].decode().rstrip('\x00')
    number_of_chunks = ceil(file_size / CHUNK_SIZE)
    print("receive " + file_name)
    chunks_list = await get_chunks(file_name, number_of_chunks, peers_list)
    await write_into_file(chunks_list, file_name)
    return True

async def write_into_file(chunks_list: list, file_name):

    try:
        # make P2P-Downloads directory
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, 'P2P-Downloads')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        file_path = os.path.join(final_directory, file_name)
        file = open(file_path, "wb")
        for chunk in chunks_list:
            for data in chunk:
                file.write(data)
        file.close()

    except Exception as e:
        print(e)

async def get_chunks(file_name: str, num_of_chunks: int, peers_list: list)->list:
    tasks = []
    chuncks_for_peer = num_of_chunks / len(peers_list)
    chunk_number = 0
    for i, peer in enumerate(peers_list):
        peer_chunks_list = []
        while chunk_number < num_of_chunks and floor(chunk_number / chuncks_for_peer) == i:
            peer_chunks_list.append(chunk_number)
            chunk_number += 1
        tasks.append(get_chunk(file_name, peer_chunks_list, peer, peers_list))
    chunks_list = await asyncio.gather(*tasks)
    return chunks_list

async def get_chunk(file_name: str, chunks_list: list, peer_ip: str, peers_list: list)->list:
    index_for_failer = 0 # If the read fail then index increase for read from next peer
    while index_for_failer < len(peers_list):
        try:
            result = []
            reader, writer = await asyncio.open_connection(peer_ip, 12346)
            for chunk_number in chunks_list:
                message = [header_struct_generator(REQUEST_CODES["REQUEST_FILE"], struct.calcsize(REQUEST_FILE_PACKING)),
                            struct.pack(REQUEST_FILE_PACKING, file_name.encode(), chunk_number)]
                for item in message:
                    writer.write(item)
                    await writer.drain()
                data = await reader.read(struct.calcsize(SEND_FILE_PACKING))
                result.append(data)
                print("receive chunk number " + str(chunk_number) + " from " + peer_ip)
            writer.close()
            await writer.wait_closed()
            return result
        except Exception as e:
            print(e)
            peer_ip = peers_list[index_for_failer]
            index_for_failer +=1
    raise Exception("can't recieve the file " + file_name + " from any peer.\nconnection fail")
    

async def peer_connected_handler(reader, writer):
    print(writer.get_extra_info('peername'), " - connected")

    while True:
        data_header = await reader.read(struct.calcsize(HEADER_PACKING))
        if not data_header:
            writer.close()
            await writer.wait_closed()
            break
        message_code, payload_size = struct.unpack(HEADER_PACKING, data_header)
        payload = await reader.read(payload_size)
        file_name, chunk_number = struct.unpack(REQUEST_FILE_PACKING, payload)
        file_name = file_name.decode().rstrip('\x00')
        print("send chunk_number " + str(chunk_number))
        try:
            file = open(file_name, "rb")
            file.seek((chunk_number) * CHUNK_SIZE)
            chunk = file.read(CHUNK_SIZE)
            writer.write(chunk)
            await writer.drain()
            file.close()
        except Exception as e:
            print(e)

async def peers_connection(host = '0.0.0.0', port = '12346'):
    server = await asyncio.start_server(peer_connected_handler, host, port)
    await server.serve_forever()

def print_success_connection():
    print('''    -----------------------------------------
    | The connection was made successfully  |
    -----------------------------------------''')

    print()

    print('''    |---------|  ~~~~~~~> |---------| 
    |...Peer..|           |...Peer..|
    |---------|           |---------| 
    \          \           \         \ 
     \..........\           \.........\  ''')

    print()
async def main():
    print('''    ********************************************
    Hello and welcome to our P2P application!
    Here you can share files with the computers
    in your network
    ********************************************''')

    f1 = loop.create_task(tracker_connection())
    f2 = loop.create_task(peers_connection())
    await asyncio.wait([f1])
  
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
        loop.close()
    except KeyboardInterrupt:
        pass
