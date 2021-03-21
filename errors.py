import time


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


class Errors:
    def __init__(self, timeout_sec):
        self.timer = Timer(timeout_sec)
        self._state = False

