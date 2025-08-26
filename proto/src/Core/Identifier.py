from __future__ import annotations
from typing import Optional
from Hash import Hash

class Identifier:
    def __init__(self, value: Optional[str | int] = None):
        if value is None:
            self.hash: int = 0
            self.dbg_name: str = ""
        elif isinstance(value, str):
            self.hash = Hash.generate_fnv_hash(value)
            self.dbg_name = value
        elif isinstance(value, int):
            self.hash = value
            self.dbg_name = ""
        else:
            raise TypeError("Identifier must be initialized with str, int, or None")

    def __eq__(self, other: Identifier) -> bool:
        return self.hash == other.hash

    def __ne__(self, other: Identifier) -> bool:
        return self.hash != other.hash

    def __int__(self) -> int:
        return self.hash

    def get_dbg_name(self) -> str:
        return self.dbg_name

    def __hash__(self) -> int:
        return self.hash