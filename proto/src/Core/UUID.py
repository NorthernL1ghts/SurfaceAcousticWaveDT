import random

class UUID:
    def __init__(self, value: int = None, bits: int = 64):
        if bits not in (32, 64):
            raise ValueError("UUID must be 32 or 64 bits")
        self.bits = bits
        mask = (1 << bits) - 1

        if value is None:
            # Random number in range
            self.value = random.getrandbits(bits)
        else:
            # Force into correct bit size
            self.value = value & mask

    def __int__(self) -> int:
        return self.value

    def __eq__(self, other) -> bool:
        return isinstance(other, UUID) and self.value == other.value and self.bits == other.bits

    def __hash__(self) -> int:
        # Include bits in hash so 32/64 UUIDs with same number aren't "equal"
        return hash((self.value, self.bits))

    def __repr__(self) -> str:
        return f"UUID({self.value}, {self.bits}-bit)"