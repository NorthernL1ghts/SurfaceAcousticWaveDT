from typing import Callable, Generic, TypeVar, List, Optional

T = TypeVar("T")
TReturn = TypeVar("TReturn")

class Delegate(Generic[TReturn]):
    """Single-cast delegate for a callback function."""

    def __init__(self):
        self._callback: Optional[Callable] = None

    def bind(self, func: Callable[..., TReturn]):
        """Bind a free function, lambda, or method."""
        self._callback = func

    def unbind(self):
        """Remove binding."""
        self._callback = None

    def is_bound(self) -> bool:
        return self._callback is not None

    def __bool__(self):
        return self.is_bound()

    def invoke(self, *args, **kwargs) -> TReturn:
        if not self.is_bound():
            raise RuntimeError("Trying to invoke unbound delegate.")
        return self._callback(*args, **kwargs)


class MulticastDelegate(Generic[TReturn]):
    """Multicast delegate for multiple callbacks."""

    def __init__(self):
        self._callbacks: List[Callable[..., TReturn]] = []

    def bind(self, func: Callable[..., TReturn]):
        """Add a callback."""
        if func not in self._callbacks:
            self._callbacks.append(func)

    def unbind(self, func: Callable[..., TReturn]):
        """Remove a callback."""
        if func in self._callbacks:
            self._callbacks.remove(func)

    def is_bound(self) -> bool:
        return len(self._callbacks) > 0

    def __bool__(self):
        return self.is_bound()

    def invoke(self, *args, **kwargs):
        if not self.is_bound():
            raise RuntimeError("Trying to invoke unbound multicast delegate.")
        # Iterate over a copy to prevent modification during iteration
        for callback in list(self._callbacks):
            callback(*args, **kwargs)