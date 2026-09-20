"""Print messages to an array for testing purposes."""

from Application.Printer import Printer


class TestPrinter(Printer):
    """Print messages to an array for testing purposes."""

    __test__ = False
    
    def __init__(self, outputArray: list[str]):
        """Initialize the TestPrinter with the specified output array."""
        self.outputArray = outputArray

    def print(self, message: str) -> None:
        """Print a message to an array for testing purposes."""
        self.outputArray.append(message)
