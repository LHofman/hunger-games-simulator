import random
from typing import TypeVar

from Application.Port.IRandomizer import IRandomizer

T = TypeVar("T")

class Randomizer(IRandomizer):

  def chooseOne(self, items: list[T]) -> T:
    return random.choice(items)
