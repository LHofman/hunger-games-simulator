"""Replace text terms in the game state."""

from domain.event_rule import TextAndTerms
from domain.event_rules_list import event_rules_list
from domain.types import GameRoundState


def replace_text_terms(game_state: GameRoundState) -> TextAndTerms:
    """Replace text and terms in the event based on the current game state."""
    text_and_terms: TextAndTerms = {
        'text': game_state['event']['text'],
        'tributes': [],
        'terms': {},
    }

    for event_rule in event_rules_list:
        text_and_terms = event_rule.replace_text_terms(game_state, text_and_terms)
            
    return text_and_terms
