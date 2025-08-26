from typing import Final

class Hash:
    # Precompute the CRC32 table at module load
    POLYNOMIAL: Final[int] = 0xEDB88320
    NUM_BYTES: Final[int] = 256
    NUM_ITERATIONS: Final[int] = 8

    @staticmethod
    def gen_crc32_table():
        table = [0] * Hash.NUM_BYTES
        for byte in range(Hash.NUM_BYTES):
            crc = byte
            for _ in range(Hash.NUM_ITERATIONS):
                mask = -(crc & 1)
                crc = (crc >> 1) ^ (Hash.POLYNOMIAL & mask)
            table[byte] = crc
        return table

# Generate the table once
crc32_table = Hash.gen_crc32_table()

# Optional static checks
assert len(crc32_table) == 256
assert crc32_table[1] == 0x77073096
assert crc32_table[255] == 0x2D02EF8D

class Hash:
    @staticmethod
    def crc32(data: str) -> int:
        crc = 0xFFFFFFFF
        for c in data:
            crc = crc32_table[(crc ^ ord(c)) & 0xFF] ^ (crc >> 8)
        return crc ^ 0xFFFFFFFF

    @staticmethod
    def crc32_bytes(data: bytes) -> int:
        crc = 0xFFFFFFFF
        for b in data:
            crc = crc32_table[(crc ^ b) & 0xFF] ^ (crc >> 8)
        return crc ^ 0xFFFFFFFF