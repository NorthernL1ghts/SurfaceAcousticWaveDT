import time

class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the start time to now."""
        self._start = time.perf_counter()

    def elapsed(self) -> float:
        """
        Return the elapsed time in seconds since the timer was started or last reset.
        """
        return time.perf_counter() - self._start

    def elapsed_millis(self) -> float:
        """
        Return the elapsed time in milliseconds since the timer was started or last reset.
        """
        return self.elapsed() * 1000.0

    def __repr__(self) -> str:
        return f"Timer(elapsed={self.elapsed():.6f}s)"