"""Event rule that handles effects on the gamestate based on multiple tributes involved in an event."""

import random

from domain.event_rule import EventRule, TextAndTerms
from domain.types import Event, GameRoundState, GameRoundStateWithoutEvent


class MultipleTributes(EventRule):
    """Event rule that handles effects on the gamestate based on multiple tributes involved in an event."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the number of tributes involved in the event."""
        if 'tributes' not in event:
            return True

        return (
            len(game_state['tributes_remaining_this_round']) + 1
            >= event['tributes']
        )

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on the number of tributes involved in the event."""
        text = text_and_terms['text']
        tributes = text_and_terms.get('tributes', [])

        while text.find('(Tribute') > -1:
            tribute = random.choice(
                list(game_state['tributes_remaining_this_round'].values()),
            )
            del game_state['tributes_remaining_this_round'][tribute['name']]

            tributes.append(tribute)
            text = text.replace(f'(Tribute{len(tributes)})', tribute['name'])

        return {**text_and_terms, 'text': text, 'tributes': tributes}
