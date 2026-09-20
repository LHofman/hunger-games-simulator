"""Abstract base class for printing messages."""

from abc import ABC


class Printer(ABC):
    """Abstract base class for printing messages. Subclasses should implement the print method."""

    def print(self, message: str) -> None:
        """Print a message. Subclasses should override this method to provide specific printing behavior."""
        print(message)
