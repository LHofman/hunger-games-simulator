"""Prints messages to a file."""

from Application.Printer import Printer


class FilePrinter(Printer):
    """Print messages to a file."""

    def __init__(self, filePath: str):
        """Initialize the FilePrinter with the specified file path."""
        self.filePath = filePath

    def print(self, message: str) -> None:
        """Print a message to a file."""
        outputFile = open(self.filePath, 'a', encoding='utf-8')
        outputFile.write(f'\n{str(message)}')
        outputFile.close()
