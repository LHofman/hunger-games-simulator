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

  def print(self) -> None:
    self.__printer.print(self.__text)
    