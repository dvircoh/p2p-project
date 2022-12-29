from peer import *
import asyncio
import subprocess

 #TODO: all cases check failed

async def main():
    print("Test: begin")
    tracker_process = subprocess.Popen('python tracker.py', creationflags=8, close_fds=True)
    other_peer_process = subprocess.Popen('python other_peer_test.py', creationflags=8, close_fds=True)
    tracker_ip = "127.0.0.1"
    result = await init(tracker_ip)
    assert result, "add user to tracker failed"
    print("Test: init success")
    message = add_file_handler("hello_world")
    result = await send_to_tracker(tracker_ip, message)
    message = add_file_handler("crc.py")
    result = await send_to_tracker(tracker_ip, message)
    assert result, "add file failed"
    print("Test: add file success")
    await actions(tracker_ip, 4)
    message = send_files_list_handler()
    result = await send_and_recv_tracker(tracker_ip, message)
    result = eval(result.decode('utf-8'))
    print(result)
    print(type(result))
    await actions(tracker_ip, 5)
    #assert result, "request files list failed"
    print("Test: request files list success")

    message = await peers_connection("127.0.0.1")
    # await send_to_tracker(tracker_ip, message) #TODO add some check on peers_connection in "peers.py"
    # await actions(tracker_ip, 6)

    message = remove_file_handler("hello_world")
    result = await send_to_tracker(tracker_ip, message)
    assert result, "remove file failed"
    print("Test: remove file success")
    message = remove_user_handler()
    result = await send_to_tracker(tracker_ip, message)
    assert result, "disconnecting failed"
    print("Test: disconnecting success")

    # Close subprocesses (very importent for free the ports)
    other_peer_process.kill()
    tracker_process.kill()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
