import shutil
import os

class DataTransfer:
    def __init__(self, source_path, destination_path):
        """
        Initialize the DataTransfer with source and destination file paths.
        """
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"Source file '{source_path}' does not exist.")
        self.source_path = source_path
        self.destination_path = destination_path

    def transfer(self):
        """
        Move any file, regardless of extension.
        """
        # Ensure destination folder exists
        os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
        shutil.move(self.source_path, self.destination_path)
        print(f"File moved from '{self.source_path}' to '{self.destination_path}'.")
