"""Event rule that handles effects on the gamestate based on the current tribute."""

from domain.event_rule import EventRule, TextAndTerms
from domain.types import GameRoundState


class CurrentTribute(EventRule):
    """Event rule that handles effects on the gamestate based on the current tribute."""

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the current tribute."""
        text = text_and_terms['text'].replace(
            '(Player1)',
            game_state['current_tribute']['name'],
        )

        return {
            **text_and_terms,
            'text': text,
            'players': [game_state['current_tribute']],
        }
