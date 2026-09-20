"""Prints messages to a file."""

from application.printer import Printer


class FilePrinter(Printer):
    """Print messages to a file."""

    def __init__(self, file_path: str):
        """Initialize the FilePrinter with the specified file path."""
        self.file_path = file_path

    def print(self, message: str) -> None:
        """Print a message to a file."""
        output_file = open(self.file_path, 'a', encoding='utf-8')
        output_file.write(f'\n{str(message)}')
        output_file.close()
