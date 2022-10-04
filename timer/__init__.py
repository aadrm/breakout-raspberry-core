import time


class Timer:

    time_datum = 0
    time_now = time.time()

    def __init__(self):
        self.time_datum = self.time_now

    def new_datum(self) -> None:
        self.time_datum = self.time_now
        return lap_time

    def time_passed(self) -> float:
        return self.time_now - self.time_datum
