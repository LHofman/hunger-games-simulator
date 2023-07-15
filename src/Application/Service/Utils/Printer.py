from Application.Port.IPrinter import IPrinter

class Printer(IPrinter):

  def print(self, text) -> None:
    print(text)
