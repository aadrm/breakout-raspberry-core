import time


class Timer:

    time_datum = 0

    def __init__(self):
        self.time_datum = time.time()

    def new_datum(self) -> None:
        self.time_datum = time.time()

    def time_passed(self) -> float:
        return time.time() - self.time_datum
