"""Event rule that handles effects on the gamestate based on deaths."""

import re

from Domain.EventRule import EventRule, TextAndTerms
from Domain.EventRules.TributesData import TributesData
from Domain.types import GameRoundState


class Deaths(EventRule):
    """Event rule that handles effects on the gamestate based on deaths."""

    def handleEventEffects(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> None:
        """Handle the effects of deaths in the event on the game state."""
        event = gameState['event']

        if 'deaths' not in event: return

        players = textAndTerms.get('players', [])

        for death in event['deaths']:
            match = re.search(r'\d+', death)
            if not match: raise ValueError(
                f'No number found in death term: {death}',
            )

            index = int(match.group()) - 1
            playerName = players[index]['name']
            gameState['recentDeaths'].append(
                (playerName, players[index]['district']),
            )
            TributesData.updateTributesData(
                gameState,
                players[index],
                'time of death',
                '',
                gameState['exactTime'],
            )
            TributesData.updateTributesData(
                gameState,
                players[index],
                'district',
                '',
                players[index]['district'],
            )

            for (name, _tribute) in gameState['playersAlive'].items():
                if playerName in _tribute['groupedWith']:
                    gameState['playersAlive'][name]['groupedWith'].remove(
                        playerName,
                    )

            del gameState['playersAlive'][playerName]
