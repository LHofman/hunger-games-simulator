"""Event rule that handles effects on the gamestate based on deaths."""

import re

from domain.event_rule import EventRule, TextAndTerms
from domain.event_rules.tributes_data import TributesData
from domain.types import GameRoundState


class Deaths(EventRule):
    """Event rule that handles effects on the gamestate based on deaths."""

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of deaths in the event on the game state."""
        event = game_state['event']

        if 'deaths' not in event: return

        players = text_and_terms.get('players', [])

        for death in event['deaths']:
            match = re.search(r'\d+', death)
            if not match: raise ValueError(
                f'No number found in death term: {death}',
            )

            index = int(match.group()) - 1
            player_name = players[index]['name']
            game_state['recent_deaths'].append(
                (player_name, players[index]['district']),
            )
            TributesData.update_tributes_data(
                game_state,
                players[index],
                'time of death',
                '',
                game_state['exact_time'],
            )
            TributesData.update_tributes_data(
                game_state,
                players[index],
                'district',
                '',
                players[index]['district'],
            )

            for (name, _tribute) in game_state['players_alive'].items():
                if player_name in _tribute['grouped_with']:
                    game_state['players_alive'][name]['grouped_with'].remove(
                        player_name,
                    )

            del game_state['players_alive'][player_name]
