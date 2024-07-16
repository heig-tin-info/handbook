import time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.lap_times = []
        self.running = False

    def reset(self):
        self.start_time = None
        self.lap_times = []
        self.running = False

    def start(self):
        if self.running:
            return
        self.start_time = time.time()
        self.running = True

    def lap(self):
        if self.running:
            current_time = time.time()
            lap_time = current_time - self.start_time
            self.lap_times.append(lap_time)
            self.start_time = current_time
        else:
            self.start()

    def stop(self):
        if self.running:
            final_time = time.time() - self.start_time
            self.lap_times.append(final_time)
            self.running = False

    @property
    def laps(self):
        return self.lap_times

    @property
    def total(self):
        return sum(self.lap_times)
