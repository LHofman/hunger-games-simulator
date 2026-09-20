"""Base class for event rules."""

from abc import ABC

from Domain.types import (
    Event,
    GameRoundState,
    GameRoundStateWithoutEvent,
    Tribute,
)
from typing import TypedDict
from typing_extensions import NotRequired, Required


class TextAndTerms(TypedDict):
    """Represent the text and terms associated with an event."""

    text: Required[str]
    players: NotRequired[list[Tribute]]
    terms: NotRequired[dict[str, str]]


class EventRule(ABC):
    """Abstract base class for event rules that define how events affect the game state."""

    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the game state."""
        return True

    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the game state."""
        return textAndTerms

    def handleEventEffects(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> None:
        """Handle the effects of the event on the game state."""
        return
