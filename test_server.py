from NTFS_File_Recover.file_offset import listen, send_data, send_quit

from time import sleep
from threading import Thread
from functools import partial

PORT = 7891
DATA = b"abcd1234"


def stop_server():
    sleep(2)
    send_quit(PORT)


stop = Thread(target=stop_server)

thr = Thread(target=partial(send_data, PORT, DATA))
thr.start()
stop.start()

data = listen(PORT)
thr.join()

print(data)
