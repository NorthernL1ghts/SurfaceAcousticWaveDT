import zlib

class Hash:
    FNV_PRIME = 16777619
    OFFSET_BASIS = 2166136261

    @staticmethod
    def generate_fnv_hash(s: str) -> int:
        """Generate FNV-1a 32-bit hash for a string."""
        hash_ = Hash.OFFSET_BASIS
        for c in s:
            hash_ ^= ord(c)
            hash_ = (hash_ * Hash.FNV_PRIME) & 0xFFFFFFFF  # ensure 32-bit overflow
        # final null byte
        hash_ ^= 0
        hash_ = (hash_ * Hash.FNV_PRIME) & 0xFFFFFFFF
        return hash_

    @staticmethod
    def crc32(s: str) -> int:
        """Compute CRC32 of a string."""
        return zlib.crc32(s.encode('utf-8')) & 0xFFFFFFFF