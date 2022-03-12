"""Time model."""


class Time:
    """Model the progress of time."""

    def __init__(self, time_step: float) -> None:
        self.elapsed_time = 0.0
        self.time_step = time_step
        self.calculations = 30

    def update(self) -> None:
        """Update the time."""
        self.elapsed_time += self.time_step

    def slower(self) -> None:
        self.calculations = max(self.calculations - 1, 1)

    def faster(self) -> None:
        self.calculations = min(self.calculations + 1, 120)
