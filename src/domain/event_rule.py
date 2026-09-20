"""Base class for event rules."""

from abc import ABC

from domain.types import (
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

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the game state."""
        return True

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the game state."""
        return text_and_terms

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of the event on the game state."""
        return
