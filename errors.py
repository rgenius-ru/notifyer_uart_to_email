import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self, timeout):
        self._previous_time = None
        self.is_started = False
        self._timeout = timeout

    def start(self):
        """Start a new timer"""
        self._previous_time = time.perf_counter()
        self.is_started = True

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if not self.is_started:
            raise TimerError(f"Timer {self.__str__()} is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self._previous_time
        self._previous_time = None
        self.is_started = False
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

    def time_is_over(self):
        if not self.is_started:
            self.start()
            return True

        time_now = time.perf_counter()
        time_difference = time_now - self._previous_time
        if time_difference > self._timeout:
            self._previous_time = time_now
            return True

        return False

    def restart(self):
        self.start()


class Errors:
    def __init__(self, timeout_sec=3600):
        self.timer = Timer(timeout_sec)
        self._state = False

