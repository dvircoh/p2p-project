import peer
# import tracker
# import threading 

def main():
    print("Test: begin")
    # tracker_thread = threading.Thread(target=tracker.main)
    # tracker_thread.start()
    tracker_ip = "127.0.0.1"
    result = peer.init(tracker_ip)
    assert result, "add file failed"
    print("Test: init success")
    message = peer.peer_request_handler.add_file_handler("hello_world")
    result = peer.send_to_tracker(tracker_ip, message)
    assert result, "add file failed"
    print("Test: add file success")
    

if __name__ == '__main__':
    main()
