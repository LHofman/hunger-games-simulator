from Application.Port.IPrinter import IPrinter
from Domain.Event import Event
from Domain.Tributes import Tributes

class EventPrinter:

  def __init__(self, printer: IPrinter) -> None:
    self.__printer = printer

  def print(self, tributes: Tributes, event: Event) -> None:
    text = event.getText()

    index = 0
    while (text.find("(Player") > -1):
      tribute = tributes.getTributeFromEventText("Player%d" % (index + 1))
      text = text.replace("(Player%d)" % (index + 1), tribute.getName())
      index += 1

    self.__printer.print(text)
