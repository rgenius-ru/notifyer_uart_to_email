import time
from uart import BaseStation
from mail_sender import notify_all
from errors import Errors
from config import smtp_server, smtp_port, sender_email, password, error_send_interval, serial_port

error1 = Errors(timeout_sec=error_send_interval)
error2 = Errors(timeout_sec=error_send_interval)
error3 = Errors(timeout_sec=error_send_interval)
error4 = Errors(timeout_sec=error_send_interval)

pc_str = '[PC program]'

base_station = BaseStation(port=serial_port)
base_station.start()

while not base_station.is_connected:  # Wait connection
    if base_station.is_stopped:
        print(pc_str, 'Stop')
        exit(1)
    print(pc_str, 'Not connected')
    time.sleep(1)

while True:
    if base_station.is_stopped:
        break

    try:
        time.sleep(1)

        if base_station.errors:
            message = ''

            for error in base_station.errors:
                if error == 1 and error1.timer.time_is_over():
                    message += 'Error ' + str(error) + '   '
                if error == 2 and error2.timer.time_is_over():
                    message += 'Error ' + str(error) + '   '
                if error == 3 and error3.timer.time_is_over():
                    message += 'Error ' + str(error) + '   '
                if error == 4 and error4.timer.time_is_over():
                    message += 'Error ' + str(error) + '   '

            if message:
                print(pc_str, 'Email message:', message)
                notify_all(message, smtp_server, smtp_port, sender_email, password)

            base_station.errors = []

    except KeyboardInterrupt:
        base_station.stop()
        break
