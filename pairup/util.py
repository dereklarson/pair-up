import time


class TimeoutException(Exception):
    pass


class Timeout:
    def __init__(self, timeout_seconds):
        self.timeout_seconds = timeout_seconds

    def __enter__(self):
        self.death_time = time.time() + self.timeout_seconds

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def check_time(self):
        if time.time() > self.death_time:
            raise TimeoutException(f"Timeout after {self.timeout_seconds}s")
