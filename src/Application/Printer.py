from abc import ABC

class Printer(ABC):
  def print(self, message: str) -> None:
    print(message)
