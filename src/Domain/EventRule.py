from abc import ABC
from Domain.types import Event, GameRoundState, GameRoundStateWithoutEvent, Tribute
from typing import TypedDict
from typing_extensions import NotRequired, Required

class TextAndTerms(TypedDict):
    text: Required[str]
    players: NotRequired[list[Tribute]]
    terms: NotRequired[dict[str, str]]

class EventRule(ABC):
    def canPlayEvent(self, event: Event, gameState: GameRoundStateWithoutEvent) -> bool:
        return True

    def replaceTextTerms(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> TextAndTerms:
        return textAndTerms

    def handleEventEffects(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> None:
        return
