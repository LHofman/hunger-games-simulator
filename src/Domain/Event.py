from Application.Port.IPrinter import IPrinter

class Event:
  
  def __init__(
    self,
    printer: IPrinter,
    name: str,
    text: str
  ) -> None:
    self.__printer = printer
    self.__name = name
    self.__text = text

  def print(self, tributeName: str) -> None:
    text = self.__text

    text = text.replace("(Player1)", tributeName)

    self.__printer.print(text)
    