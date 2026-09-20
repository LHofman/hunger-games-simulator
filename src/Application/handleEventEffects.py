"""Handle the effects of events in the game."""

from Domain.EventRule import TextAndTerms
from Domain.eventRulesList import eventRulesList
from Domain.types import GameRoundState


def handleEventEffects(
    gameState: GameRoundState,
    textAndTerms: TextAndTerms,
) -> None:
    """Apply the effects of an event to the game state based on the provided text and terms."""
    for eventRule in eventRulesList:
        eventRule.handleEventEffects(gameState, textAndTerms)
