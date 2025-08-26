from typing import TypeVar, Generic
import ctypes

T = TypeVar('T')


class Buffer:
    def __init__(self, size: int = 0):
        self.data: bytearray | None = None
        self.size: int = 0
        if size > 0:
            self.allocate(size)

    @staticmethod
    def copy(other: 'Buffer') -> 'Buffer':
        result = Buffer(other.size)
        if other.data is not None:
            result.data[:] = other.data[:]
        return result

    def allocate(self, size: int):
        self.release()
        self.data = bytearray(size)
        self.size = size

    def release(self):
        self.data = None
        self.size = 0

    def as_type(self, typ: type[T]) -> list[T]:
        """Return the buffer interpreted as a list of type T (like casting)."""
        if self.data is None:
            return []
        # Compute how many elements of type T fit
        element_size = ctypes.sizeof(typ)
        count = self.size // element_size
        arr = (typ * count).from_buffer(self.data)
        return list(arr)

    def __bool__(self) -> bool:
        return self.data is not None


class ScopedBuffer:
    def __init__(self, buffer_or_size: int | Buffer):
        if isinstance(buffer_or_size, Buffer):
            self._buffer = buffer_or_size
        else:
            self._buffer = Buffer(buffer_or_size)

    def __del__(self):
        self._buffer.release()

    @property
    def data(self) -> bytearray | None:
        return self._buffer.data

    @property
    def size(self) -> int:
        return self._buffer.size

    def as_type(self, typ: type[T]) -> list[T]:
        return self._buffer.as_type(typ)

    def __bool__(self) -> bool:
        return bool(self._buffer)