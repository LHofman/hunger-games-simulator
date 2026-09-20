"""Event rule that handles effects on the gamestate based on possessions in the event."""

import random
import re

from domain.event_rule import EventRule, TextAndTerms
from domain.types import (
    Event,
    GameRoundState,
    GameRoundStateWithoutEvent,
)


class Possessions(EventRule):
    """Event rule that handles effects on the gamestate based on possessions in the event."""

    def can_play_event(
        self,
        event: Event,
        game_state: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on the possessions required in the event."""
        if 'requires_possessions' not in event:
            return True

        for possession in event['requires_possessions']:
            tribute = game_state['current_tribute']
            tribute_has_possession = tribute.has_possession(
                possession['type'],
                possession['value'],
            )

            if possession.get('inverse') and tribute_has_possession:
                return False

            if not possession.get('inverse') and not tribute_has_possession:
                return False

        return True

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on possessions in the event."""
        text = text_and_terms['text']
        terms = text_and_terms.get('terms', {})

        index = text.find('(Possession:')
        while index > -1:
            match = re.search(r'\d', text[index:])
            if not match:
                raise ValueError(
                    f'No number found in possession term: {text[index:]}',
                )

            number = int(match.group())
            number_index = match.start()

            possession_type = text[
                (index + len('(Possession:')) : (index + number_index)
            ]
            current_tribute = game_state.get('current_tribute')
            possession = random.choice(
                current_tribute.possessions[possession_type],
            )
            term = f'(Possession:{possession_type}{number})'
            terms[term] = possession

            text = text.replace(term, possession)

            index = text.find('(Possession:')

        return {**text_and_terms, 'text': text, 'terms': terms}

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of possessions in the event on the game state."""
        self._handle_add_possessions(game_state, text_and_terms)
        self._handle_remove_possessions(game_state, text_and_terms)

    def _handle_add_possessions(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ):
        event = game_state['event']

        if 'add_possessions' not in event:
            return

        tributes = text_and_terms.get('tributes', [])

        for possession in event['add_possessions']:
            value = possession['value']
            if value in text_and_terms.get('terms', {}):
                value = text_and_terms.get('terms', {})[value]

            tribute_name = tributes[possession['tribute'] - 1].name
            tribute = game_state['tributes_alive'][tribute_name]

            tribute.add_possession(
                game_state['options'],
                possession['type'],
                value,
            )

    def _handle_remove_possessions(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ):
        event = game_state['event']

        if 'remove_possessions' not in event:
            return

        tributes = text_and_terms.get('tributes', [])

        for possession in event['remove_possessions']:
            value = possession['value']
            if value in text_and_terms.get('terms', {}):
                value = text_and_terms.get('terms', {})[value]

            tribute_name = tributes[possession['tribute'] - 1].name
            tribute = game_state['tributes_alive'][tribute_name]

            tribute.remove_possession(possession['type'], value)
