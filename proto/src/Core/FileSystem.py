from pathlib import Path
from Buffer import Buffer

class FileSystem:
    @staticmethod
    def read_file_binary(filepath: str | Path) -> Buffer:
        """
        Reads a file in binary mode and returns its contents in a Buffer.
        Returns an empty Buffer if the file cannot be opened or is empty.
        """
        path = Path(filepath)
        if not path.is_file():
            return Buffer()  # file doesn't exist

        size = path.stat().st_size
        if size == 0:
            return Buffer()  # file is empty

        buf = Buffer(size)
        with path.open("rb") as f:
            buf.data[:] = f.read(size)
        return buf