import time


class Timer:
    def __init__(self, description="Default timer"):
        self.description = description

    def __enter__(self):
        self.start = time.perf_counter_ns()

    def __exit__(self, type, value, traceback):
        self.end = time.perf_counter_ns()
        print(f"{self.description}: {(self.end - self.start) / 1000} ms")
