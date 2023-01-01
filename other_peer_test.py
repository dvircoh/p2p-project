from peer import *
import asyncio

 #TODO: all cases check failed

async def main():
    tracker_ip = "127.0.0.1"
    await init(tracker_ip)
    await asyncio.sleep(3)

    # Add 2 files and sent them to tha main peer test

    message = add_file_handler("hello_world")
    await send_to_tracker(tracker_ip, message)
    message = add_file_handler("IEEE-spec.pdf")
    await send_to_tracker(tracker_ip, message)

    send_files_list_message = send_files_list_handler()
    files_list_result = await send_and_recv_tracker(tracker_ip, send_files_list_message)

    message = await peers_connection('0.0.0.0', "12346")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
