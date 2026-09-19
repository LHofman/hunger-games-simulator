from Application.Printer import Printer

class TestPrinter(Printer):
    __test__ = False
    
    def __init__(self, outputArray: list[str]):
        self.outputArray = outputArray

    def print(self, message: str) -> None:
        self.outputArray.append(message)
