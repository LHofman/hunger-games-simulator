"""Event rule that handles effects on the gamestate based on other terms in the event text."""

import random
import re

from domain.event_rule import EventRule, TextAndTerms
from domain.types import GameRoundState


class OtherTerms(EventRule):
    """Event rule that handles effects on the gamestate based on other terms in the event text."""

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on other terms in the event text."""
        text = text_and_terms['text']
        terms = text_and_terms.get('terms', {})

        for key, values in game_state.get('other_terms').items():
            index = text.find(f'({key}')
            while index > -1:
                match = re.search(r'\d', text[index:])
                if not match:
                    raise ValueError(
                        f'No number found in other term: {text[index:]}',
                    )

                number = int(match.group())
                term = f'({key}{number})'

                value = random.choice(values)
                terms[term] = value

                text = text.replace(term, value)

                index = text.find(f'({key}')

        return {**text_and_terms, 'text': text, 'terms': terms}
