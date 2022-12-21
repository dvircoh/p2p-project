import peer
import asyncio
 #TODO: all cases check failed

async def main():
    print("Test: begin")
    tracker_ip = input("please enter ip in order to connect tracker: ")
    result = await peer.init(tracker_ip)
    assert result, "add user to tracker failed"
    print("Test: init success")
    message = peer.peer_request_handler.add_file_handler("hello_world")
    result = await peer.send_to_tracker(tracker_ip, message)
    assert result, "add file failed"
    print("Test: add file success")
    message = peer.peer_request_handler.send_files_list_handler()
    result = await peer.send_and_recv_tracker(tracker_ip, message)
    result = eval(result.decode('utf-8'))
    print(result)
    print(type(result))
    await peer.actions(tracker_ip, 5)
    #assert result, "request files list failed"
    print("Test: request files list success")
    message = peer.peer_request_handler.remove_file_handler("hello_world")
    result = await peer.send_to_tracker(tracker_ip, message)
    assert result, "remove file failed"
    print("Test: remove file success")
    message = peer.peer_request_handler.remove_user_handler()
    result = await peer.send_to_tracker(tracker_ip, message)
    assert result, "disconnecting failed"
    print("Test: disconnecting success")

    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
