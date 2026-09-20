"""Handle the effects of events in the game."""

from domain.event_rule import TextAndTerms
from domain.event_rules_list import event_rules_list
from domain.types import GameRoundState


def handle_event_effects(
    game_state: GameRoundState,
    text_and_terms: TextAndTerms,
) -> None:
    """Apply the effects of an event to the game state based on the provided text and terms."""
    for event_rule in event_rules_list:
        event_rule.handle_event_effects(game_state, text_and_terms)
