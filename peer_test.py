import peer
# import tracker
# import threading 

def main():
    print("Test: begin")
    # tracker_thread = threading.Thread(target=tracker.main)
    # tracker_thread.start()
    tracker_ip = "127.0.0.1"
    peer.init(tracker_ip)
    print("Test: init success")
    message = peer.peer_request_handler.add_file_handler("hello_world")
    success = peer.send_to_tracker(tracker_ip, message)
    if success:
        print("Test: add file success")






if __name__ == '__main__':
    main()
