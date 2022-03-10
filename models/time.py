"""Time model."""

class Time:
    """Model the progress of time."""

    def __init__(self, time_step: float) -> None:
        self.elapsed_time = 0.0
        self.time_step = time_step

    def update(self) -> None:
        """Update the time."""
        self.elapsed_time += self.time_step
