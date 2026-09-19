from Application.Printer import Printer


class FilePrinter(Printer):
    def __init__(self, filePath: str):
        self.filePath = filePath

    def print(self, message: str) -> None:
        outputFile = open(self.filePath, 'a', encoding='utf-8')
        outputFile.write(f'\n{str(message)}')
        outputFile.close()
