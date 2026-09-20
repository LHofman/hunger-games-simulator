"""Event rule that handles effects on the gamestate based on tributes data in the event."""

from typing import Union

from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState, Tribute


class TributesData(EventRule):
    """Event rule that handles effects on the gamestate based on tributes data in the event."""

    def handleEventEffects(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> None:
        """Handle the effects of tributes data in the event on the game state."""
        event = gameState['event']

        if 'updateTributesData' not in event: return

        players = textAndTerms.get('players', [])

        for dataToAdd in event['updateTributesData']:
            playerName = players[dataToAdd['player'] - 1]['name']
            self.updateTributesData(
                gameState,
                gameState['playersAlive'][playerName],
                dataToAdd['type'],
                dataToAdd['operation'] if 'operation' in dataToAdd else '',
                dataToAdd['value'],
            )

    @staticmethod
    def updateTributesData(
        gameState: GameRoundState,
        tribute: Tribute,
        type: str,
        operation: str,
        value: Union[int, str],
    ):
        """Update the tributes data in the game state based on the event effects."""
        if tribute['name'] not in gameState['tributesData']:
            gameState['tributesData'][tribute['name']] = {}
        
        if type not in gameState['tributesData'][tribute['name']]:
            gameState['tributesData'][tribute['name']][type] = value
            return

        if operation == 'add':
            gameState['tributesData'][tribute['name']][type] += value # type: ignore
        elif operation == 'remove':
            gameState['tributesData'][tribute['name']][type] -= value # type: ignore
        else:
            gameState['tributesData'][tribute['name']][type] = value
            