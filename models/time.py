"""Time model."""

import time
import collections


class Time:
    """Model the progress of time."""

    def __init__(self, time_step: float) -> None:
        self.elapsed_time = 0.0
        self.time_step = time_step
        self.calculations = 30
        self._timestamp = time.time()
        self.speedups: collections.deque[float] = collections.deque(maxlen=25)

    def update(self) -> None:
        """Update the time."""
        elapsed_time = self.time_step * self.calculations
        self.elapsed_time += elapsed_time
        now = time.time()
        if now - self._timestamp != 0:     
            self.speedups.append(elapsed_time / (now - self._timestamp))
        self.speedup = sum(self.speedups) / len(self.speedups)
        self._timestamp = now

    def slower(self) -> None:
        self.calculations = max(round(self.calculations / 2), 1)

    def faster(self) -> None:
        self.calculations = min(self.calculations * 2, 120)
