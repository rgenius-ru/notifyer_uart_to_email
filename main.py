import time
from uart import BaseStation
from mail_sender import notify_all
from errors import Errors

error1 = Errors(timeout_sec=3600)
error2 = Errors(timeout_sec=3600)
error3 = Errors(timeout_sec=3600)
error4 = Errors(timeout_sec=3600)

pc_str = '[PC program]'

base_station = BaseStation()
base_station.start()

while not base_station.is_connected:  # Wait connection
    print(pc_str, 'Not connected')
    time.sleep(1)

while True:
    if base_station.is_stopped:
        if base_station.errors:
            message = None
            for error in base_station.errors:
                message = 'Error ' + str(error)
            notify_all(message)
        break

    try:
        time.sleep(1)
    except KeyboardInterrupt:
        base_station.stop()
        break
