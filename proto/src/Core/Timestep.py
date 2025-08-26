class Timestep:
    def __init__(self, time: float = 0.0):
        self.time = float(time)

    def __float__(self) -> float:
        return self.time

    def get_seconds(self) -> float:
        return self.time

    def get_milliseconds(self) -> float:
        return self.time * 1000.0

    def __repr__(self) -> str:
        return f"Timestep({self.time:.6f}s)"