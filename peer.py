import asyncio
import utils
import socket
import peer_request_handler
import sys
import struct

async def ainput(string: str) -> str:
    print(string + " ")
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

async def send_to_tracker(tracker_ip, message)->bool:
    reader, writer = await asyncio.open_connection(tracker_ip, 12345)
    for item in message:
        writer.write(item)
        await writer.drain()
    success = bool(await reader.read(1))
    writer.close()
    return success

async def send_and_recv_tracker(tracker_ip, message)->bytes:
    reader, writer = await asyncio.open_connection(tracker_ip, 12345)
    for item in message:
        writer.write(item)
        await writer.drain()

    data_header = await reader.read(struct.calcsize(utils.HEADER_PACKING))
    message_code, payload_size = struct.unpack(utils.HEADER_PACKING, data_header)
    if payload_size > 0:  # For add_user and remove_user the payload empty
        payload = await reader.read(payload_size)

    writer.close()
    return payload

# Joining the network by sending a message to the tracker
async def init(tracker_ip)->bool:
    # Create "message" as list for consistenty in send_to_tracker()
    message = [utils.header_struct_generator(utils.REQUEST_CODES["ADD_USER"], 0)]
    success = await send_to_tracker(tracker_ip, message)
    return success  

# Returns the user's choice of the action they want to perform
async def menu()->int: # TODO: check input
    choice = await ainput('''What do you want to do? (enter number)
    1. Add file
    2. Remove file
    3. Get file
    4. Disconnecting from the network
    ''')
    return int(choice)

async def tracker_connection():
    init_success = False

    # Loop for join tracker lists
    while not init_success:
        tracker_ip = input("Please enter IP of tracker ")
        init_success = await init(tracker_ip)
        if init_success:
            print("The connection was made successfully")
        else:
            print("The connection failed try again")

    while True:
        choice = await menu()
        print("choice" , choice) #TODO - delete
        await actions(tracker_ip, choice)

async def actions(tracker_ip, choice):
    if(choice == utils.REQUEST_CODES['ADD_FILE']):
        file_path = await ainput("enter file path for adding:")
        message = peer_request_handler.add_file_handler(file_path)
        if message[0] == 0: # file adding failed
            return
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("add file success")
        else:
            print("add file don't success, try again")
    elif(choice == utils.REQUEST_CODES['REMOVE_FILE']):
        file_name = await ainput("enter filename for remove:")
        message = peer_request_handler.remove_file_handler(file_name)
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("remove file success")
        else:
            print("remove file don't success, try again")
    elif(choice == utils.REQUEST_CODES['REMOVE_USER']):
        message = peer_request_handler.remove_user_handler()
        success = await send_to_tracker(tracker_ip, message)
        if success:
            print("disconnecting success")
        else:
            print("disconnecting don't success")
    elif(choice == utils.REQUEST_CODES['SEND_FILES_LIST']):
        message = peer_request_handler.send_files_list_handler()
        payload = await send_and_recv_tracker(tracker_ip, message)

async def peer_connected_handler(reader, writer):
    print(writer.get_extra_info('peername'))

async def peers_connection():
     server = await asyncio.start_server(peer_connected_handler, host='0.0.0.0', port='12346')
     await server.serve_forever()

async def main():
    print('''Hello and welcome to our P2P application!
Here you can share files with the computers in your network''')

    f1 = loop.create_task(tracker_connection())
    f2 = loop.create_task(peers_connection())
    await asyncio.wait([f1])
  
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    
