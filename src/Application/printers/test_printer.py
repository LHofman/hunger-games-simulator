"""Print messages to an array for testing purposes."""

from application.printer import Printer


class TestPrinter(Printer):
    """Print messages to an array for testing purposes."""

    __test__ = False
    
    def __init__(self, output_array: list[str]):
        """Initialize the TestPrinter with the specified output array."""
        self.output_array = output_array

    def print(self, message: str) -> None:
        """Print a message to an array for testing purposes."""
        self.output_array.append(message)
