import serial
import glob
import sys
from threading import Thread
import threading
import time

# decoder = 'ascii'
decoder = 'utf8'

pc_str = '[PC program COM listener]'


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self, timeout):
        self._start_time = None
        self._timeout = timeout
        self._previous_time = time.perf_counter()

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

    def time_is_over(self):
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        time_now = time.perf_counter()
        time_difference = time_now - self._previous_time
        if time_difference > self._timeout:
            self._previous_time = time_now
            # print(time_difference)
            return True

        return False

    def restart(self):
        self._previous_time = time.perf_counter()


class SearchingBase(Thread):
    def __init__(self, port=None, ports=None, baud=9600):
        super().__init__()
        self.baud = baud
        self._ports = ports
        self.port = port
        self.received_data = None
        self.is_connected = False
        self.is_connected = False
        self.is_right_connected = False
        self._running = True
        self.timer = Timer(2)
        self.search_timer = Timer(15)
        self.is_stopped = False
        self.errors = []
        self._serial = None

    def run(self):
        s, port = self._searching_base_station()

        if not s:
            self.stop()
            print(pc_str, 'Can not find any serial port')
            exit(1)

        self._serial = s
        self.timer.start()

        while self._running:
            try:
                self.receive()
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        self.is_stopped = True
        self._running = False

    def receive(self):
        try:
            # _serial = serial.Serial(self.port, self.baud, )
            self.received_data = self._wait_receive(self.port, _timeout=2)
        except serial.SerialException as e:
            if e.errno == 13:
                print(pc_str, 'e')
                raise e
            return None
        except OSError:
            print(pc_str, 'OSError')
            return None
        except KeyboardInterrupt:
            self.stop()

        if self.timer.time_is_over():
            self.is_connected = False
            print(pc_str, 'Connected timeout')
            return None

        if self.received_data != '':
            self.timer.restart()
            _start = self.received_data
            print(self.received_data)
            if self.received_data.count('*** Error 4 ***'):
                print(pc_str, 'Stop listening port:', self.port, 'Reason:', self.received_data)
                if 4 not in self.errors:
                    self.errors.append(4)
                self.is_stopped = True
                self.is_connected = False
                self.stop()
                return None
            if self.received_data.count('*** Error 1 ***'):
                if 1 not in self.errors:
                    self.errors.append(1)
            if self.received_data.count('*** Error 2 ***'):
                if 2 not in self.errors:
                    self.errors.append(2)
            if self.received_data.count('*** Error 3 ***'):
                if 3 not in self.errors:
                    self.errors.append(3)
            if _start == 'Sensors-DD-1.0' or _start[:3] == 'dd1' or _start[:3] == '***':
                self.is_connected = True

        # print(self.is_left_connected, self.is_right_connected)

        return self.received_data

    def _wait_receive(self, _port, _timeout=1):
        # _serial = serial.Serial(_port, self.baud, timeout=_timeout)
        _serial = self._serial
        _string = None

        if _serial.isOpen():
            # while not _serial.inWaiting():
            #     pass

            data_read = _serial.readline()
            try:
                _string = data_read.decode(decoder, errors="ignore").strip()
            except UnicodeEncodeError as err:
                print(pc_str, 'ERROR:', err)
            except KeyboardInterrupt:
                self.stop()

        return _string

    def _all_serial_ports(self):
        ports = []

        if self.port:
            ports += [self.port]

        if sys.platform.startswith('win'):
            ports += ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports += glob.glob('/dev/ttyUSB*')  # ubuntu is /dev/ttyUSB0
            ports += glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            # ports = glob.glob('/dev/tty.*')
            ports = +glob.glob('/dev/tty.SLAB_USBtoUART*')
        else:
            raise EnvironmentError('Unsupported platform')

        self._ports = ports

        return self._ports != []

    def _searching_base_station(self):
        print(pc_str, 'Base station search...')
        while True:
            if not self._all_serial_ports():
                continue

            ports_count = len(self._ports)
            print(pc_str, f'Found {ports_count} ports: ', '  '.join(self._ports))

            for _port in self._ports:
                # if _port[:-1] == '/dev/ttyUSB':
                #     continue

                print(pc_str, 'Scan port: ', _port)
                self.search_timer.start()

                try:
                    _s = serial.Serial(_port, self.baud, timeout=4)

                    while not self.search_timer.time_is_over() and _s.isOpen():
                        data = bytes('DD-Sensors\r', decoder)
                        _s.write(data)
                        _data_read = _s.readline()
                        _string = _data_read.decode(decoder, errors="ignore")

                        if _string != '':
                            print(_string.strip())

                            if _string[:-6] == 'Sensors-DD':
                                self.port = _port
                                self.is_connected = True
                                result = _s, _port
                                print(pc_str, 'Found: ', _string)
                                self.search_timer.stop()
                                return result

                    _s.close()
                except UnicodeEncodeError as err:
                    self.port = None
                    self.is_connected = False
                    self.search_timer.stop()
                    print(pc_str, 'Base station not found')
                    print(pc_str, 'ERROR:', err)
                    return None, None
                except serial.SerialException as e:
                    if e.errno == 13:
                        raise e
                    self.search_timer.stop()
                    # self.port = None
                    # self.is_connected = False
                    print(pc_str, e)
                    # return None, None
                except OSError:
                    self.port = None
                    self.is_connected = False
                    self.search_timer.stop()
                    print(pc_str, 'Base station not found')
                    return None, None

            self.port = None
            self.is_connected = False
            self.search_timer.stop()
            print(pc_str, 'Base station not found')
            return None, None

        time.sleep(1)


class BaseStation(SearchingBase):
    def __init__(self, port=None):
        super().__init__(port)


if __name__ == '__main__':
    # event = threading.Event()
    base_station = BaseStation()
    base_station.start()

    while base_station.is_alive():
        time.sleep(1)
        base_station.stop()

    print(base_station.baud, base_station.port)
