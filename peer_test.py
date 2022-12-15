import peer
# import tracker
# import threading 

def main():
    print("Test: begin")
    # tracker_thread = threading.Thread(target=tracker.main)
    # tracker_thread.start()
    tracker_ip = "127.0.0.1"
    result = peer.init(tracker_ip)
    assert result, "add user to tracker failed"
    print("Test: init success")
    message = peer.peer_request_handler.add_file_handler("hello_world")
    result = peer.send_to_tracker(tracker_ip, message)
    assert result, "add file failed"
    print("Test: add file success")
    message = peer.peer_request_handler.remove_file_handler("hello_world")
    result = peer.send_to_tracker(tracker_ip, message)
    assert result, "remove file failed"
    print("Test: remove file success")
    message = peer.peer_request_handler.send_files_list_handler()
    result = peer.send_to_tracker(tracker_ip, message)
    assert result, "request files list failed"
    print("Test: request files list success")
    message = peer.peer_request_handler.remove_user_handler()
    result = peer.send_to_tracker(tracker_ip, message)
    assert result, "disconnecting failed"
    print("Test: disconnecting success")

    
if __name__ == '__main__':
    main()
