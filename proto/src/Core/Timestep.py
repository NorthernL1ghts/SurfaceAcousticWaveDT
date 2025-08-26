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

ts = Timestep(0.016)   # ~16 ms (like a 60fps frame delta)
print(float(ts))       # 0.016
print(ts.get_seconds())       # 0.016
print(ts.get_milliseconds())  # 16.0
print(ts)              # Timestep(0.016000s)
