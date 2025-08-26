import time

class FastRandom:
    # LCG constants
    DEFAULT_SEED = 4321           # Default starting seed
    LCG_MODULUS = 2147483647      # Modulus value (m)
    LCG_MULTIPLIER = 48271        # Multiplier (a)
    LCG_INCREMENT = 0             # Increment (c)

    def __init__(self, seed: int = None):
        self.state = seed if seed is not None else FastRandom.DEFAULT_SEED

    def set_seed(self, new_seed: int):
        self.state = new_seed

    def get_current_seed(self) -> int:
        return self.state

    def get_int32(self) -> int:
        self.state = (FastRandom.LCG_MULTIPLIER * self.state + FastRandom.LCG_INCREMENT) % FastRandom.LCG_MODULUS
        return self.state

    def get_uint32(self) -> int:
        return self.get_int32() & 0xFFFFFFFF

    def get_int16(self) -> int:
        return self.get_int32() & 0xFFFF

    def get_uint16(self) -> int:
        return self.get_int16() & 0xFFFF

    def get_float64(self) -> float:
        return self.get_int32() / float(FastRandom.LCG_MODULUS)

    def get_float32(self) -> float:
        return float(self.get_float64())

    def get_float32_in_range(self, low: float, high: float) -> float:
        return low + self.get_float32() * (high - low)

    def get_float64_in_range(self, low: float, high: float) -> float:
        return low + self.get_float64() * (high - low)

    def get_int32_in_range(self, low: int, high: int) -> int:
        if low >= high:
            return low
        return low + self.get_uint32() // (0xFFFFFFFF // (high - low + 1) + 1)

    # Convenience alias methods
    def get_in_range(self, low, high):
        if isinstance(low, int) and isinstance(high, int):
            return self.get_int32_in_range(low, high)
        elif isinstance(low, float) or isinstance(high, float):
            return self.get_float32_in_range(float(low), float(high))
        else:
            raise TypeError("Unsupported type for get_in_range")

# Utility function
def get_seed_from_current_time() -> int:
    return int(time.time() * 1_000_000) & 0xFFFFFFFF