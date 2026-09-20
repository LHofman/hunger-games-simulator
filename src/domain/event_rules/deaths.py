"""Event rule that handles effects on the gamestate based on deaths."""

import re

from domain.event_rule import EventRule, TextAndTerms
from domain.types import GameRoundState


class Deaths(EventRule):
    """Event rule that handles effects on the gamestate based on deaths."""

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of deaths in the event on the game state."""
        self._handle_deaths(game_state, text_and_terms)
        self._handle_kills(game_state, text_and_terms)

    def _handle_deaths(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of deaths in the event on the game state."""
        event = game_state['event']

        if 'deaths' not in event:
            return

        tributes = text_and_terms.get('tributes', [])

        for death in event['deaths']:
            match = re.search(r'\d+', death)
            if not match:
                raise ValueError(
                    f'No number found in death term: {death}',
                )

            index = int(match.group()) - 1
            tribute_name = tributes[index].name
            game_state['recent_deaths'].append(tribute_name)
            tributes[index].mark_dead(game_state['exact_time'])

            for _tribute in game_state['tributes_alive'].values():
                if _tribute.is_grouped_with(tribute_name):
                    _tribute.ungroup_with(tribute_name)

            del game_state['tributes_alive'][tribute_name]

    def _handle_kills(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of kills in the event on the game state."""
        event = game_state['event']

        if 'add_kills' not in event:
            return

        tributes = text_and_terms.get('tributes', [])

        for kills_to_add in event['add_kills']:
            tribute = tributes[kills_to_add['tribute'] - 1]
            tribute.add_kills(kills_to_add['value'])
