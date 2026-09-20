"""Event rule that handles effects on the gamestate based on sponsors in the event text."""

import random

from domain.event_rule import EventRule, TextAndTerms
from domain.types import GameRoundState


class Sponsors(EventRule):
    """Event rule that handles effects on the gamestate based on sponsors in the event text."""

    def replace_text_terms(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on sponsors in the event text."""
        text = text_and_terms['text']

        if text.find('(Sponsor') == -1:
            return text_and_terms

        if len(game_state['sponsors']) <= 0:
            return {
                **text_and_terms,
                'text': text.replace('(Sponsor)', 'an unknown sponsor'),
            }

        is_fixed_sponsor = game_state['options'].get(
            'one_sponsor_per_tribute',
            False,
        )
        if (
            not is_fixed_sponsor
            or len(game_state['sponsors']) != game_state['total_tributes']
        ):
            return {
                **text_and_terms,
                'text': text.replace(
                    '(Sponsor)',
                    random.choice(game_state['sponsors']),
                ),
            }

        if text.find('(Sponsor::opposing)') == -1:
            sponsors = game_state['sponsors']
            current_tribute_sponsor = sponsors[
                game_state['current_tribute']['index'] - 1
            ]
            return {
                **text_and_terms,
                'text': text.replace('(Sponsor)', current_tribute_sponsor),
            }

        sponsor_index = game_state['current_tribute']['index'] - 1
        other_sponsors = (
            game_state['sponsors'][:sponsor_index]
            + game_state['sponsors'][sponsor_index + 1 :]
        )
        return {
            **text_and_terms,
            'text': text.replace(
                '(Sponsor::opposing)',
                random.choice(other_sponsors),
            ),
        }
