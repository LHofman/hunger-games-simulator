"""Event rule that handles effects on the gamestate based on tributes data in the event."""

from typing import Union

from domain.event_rule import EventRule, TextAndTerms
from domain.types import GameRoundState, Tribute


class TributesData(EventRule):
    """Event rule that handles effects on the gamestate based on tributes data in the event."""

    def handle_event_effects(
        self,
        game_state: GameRoundState,
        text_and_terms: TextAndTerms,
    ) -> None:
        """Handle the effects of tributes data in the event on the game state."""
        event = game_state['event']

        if 'update_tributes_data' not in event: return

        tributes = text_and_terms.get('tributes', [])

        for data_to_add in event['update_tributes_data']:
            tribute_name = tributes[data_to_add['tribute'] - 1]['name']
            self.update_tributes_data(
                game_state,
                game_state['tributes_alive'][tribute_name],
                data_to_add['type'],
                data_to_add['operation'] if 'operation' in data_to_add else '',
                data_to_add['value'],
            )

    @staticmethod
    def update_tributes_data(
        game_state: GameRoundState,
        tribute: Tribute,
        type: str,
        operation: str,
        value: Union[int, str],
    ):
        """Update the tributes data in the game state based on the event effects."""
        if tribute['name'] not in game_state['tributes_data']:
            game_state['tributes_data'][tribute['name']] = {}
        
        if type not in game_state['tributes_data'][tribute['name']]:
            game_state['tributes_data'][tribute['name']][type] = value
            return

        if operation == 'add':
            game_state['tributes_data'][tribute['name']][type] += value # type: ignore
        elif operation == 'remove':
            game_state['tributes_data'][tribute['name']][type] -= value # type: ignore
        else:
            game_state['tributes_data'][tribute['name']][type] = value
            