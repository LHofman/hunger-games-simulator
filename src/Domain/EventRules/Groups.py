"""Event rule that handles effects on the gamestate based on group dynamics."""

import random
import re

from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import (
    Event,
    GameRoundState,
    GameRoundStateWithoutEvent,
    GroupSizeType,
    Tribute,
)


class Groups(EventRule):
    """Event rule that handles effects on the gamestate based on group dynamics."""

    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        """Check if the event can be played based on group dynamics and game state."""
        if not self._satisfiesGroupSize(event, gameState): return False
        if not self._satisfiesCanFormGroup(event, gameState): return False
        if not self._satisfiesCanBetrayTeammates(event, gameState):
            return False

        return True

    def _satisfiesGroupSize(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'requireGroupSize' not in event: return True

        sizeType = event['requireGroupSize']['type']
        size = event['requireGroupSize']['amount']

        availableGroupTributes = 1  # Tribute themself.
        for (name) in gameState['playersRemainingThisRound'].keys():
            if name in gameState['currentTribute']['groupedWith']:
                availableGroupTributes += 1

        if (
            sizeType == GroupSizeType.EXACT
            and size != len(gameState['currentTribute']['groupedWith']) + 1
        ): return False

        if (
            sizeType == GroupSizeType.MIN
            and size > availableGroupTributes
        ): return False

        if (
            sizeType == GroupSizeType.MAX
            and size < len(gameState['currentTribute']['groupedWith']) + 1
        ): return False

        return True

    def _satisfiesCanFormGroup(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        if 'formGroup' not in event: return True

        return len(gameState['playersAlive']) > 2
    
    def _satisfiesCanBetrayTeammates(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent,
    ) -> bool:
        if gameState['options']['betrayTeammates']: return True
        if 'deaths' not in event: return True
        if 'killTeammates' not in event or not event['killTeammates']:
            return True

        for death in event['deaths']:
            if death in gameState['currentTribute']['groupedWith']:
                return False

        return True

    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> TextAndTerms:
        """Replace text and terms in the event based on group dynamics and the current game state."""
        event = gameState['event']

        if 'requireGroupSize' not in event: return textAndTerms

        aoGroupPlayersRequired = event['requireGroupSize']['amount']
        
        playersRemaining = gameState.get('playersRemainingThisRound').items()
        groupedWithPlayers: dict[str, Tribute] = {}
        for (name, player) in playersRemaining:
            if name in gameState.get('currentTribute')['groupedWith']:
                groupedWithPlayers[name] = player

        text = textAndTerms['text']
        players: list[Tribute] = textAndTerms.get('players', [])
        while (
            text.find('(Player') > -1
            and len(players) < aoGroupPlayersRequired
        ):
            player = random.choice(list(groupedWithPlayers.values()))
            del groupedWithPlayers[player['name']]
            del gameState['playersRemainingThisRound'][player['name']]

            players.append(player)
            text = text.replace(f'(Player{len(players)})', player['name'])

        return { **textAndTerms, 'text': text, 'players': players }

    def handleEventEffects(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms,
    ) -> None:
        """Handle the effects of group dynamics in the event on the game state."""
        self._handleFormGroup(gameState, textAndTerms.get('players', []))
        self._handleSplitGroup(gameState, textAndTerms.get('players', []))

    def _handleFormGroup(
        self,
        gameState: GameRoundState,
        players: list[Tribute],
    ) -> None:
        event = gameState['event']

        if 'formGroup' not in event: return

        for player in players:
            for otherPlayer in players:
                if player['name'] == otherPlayer['name']: continue

                groupedWith = (
                    gameState['playersAlive'][player['name']]['groupedWith']
                )
                if otherPlayer['name'] in groupedWith: continue
                groupedWith.append(otherPlayer['name'])

    def _handleSplitGroup(
        self,
        gameState: GameRoundState,
        players: list[Tribute],
    ) -> None:
        event = gameState['event']

        if 'splitGroup' not in event: return

        playersToSplit: list[str] = []
        for playerToSplit in event['splitGroup']:
            match = re.search(r'\d+', playerToSplit)
            if not match: raise ValueError(
                f'No number found in split group term: {playerToSplit}',
            )

            index = int(match.group()) - 1
            playersToSplit.append(players[index]['name'])
            
        for player in players:
            if player['name'] not in playersToSplit: continue
            for playerToSplit in playersToSplit:
                if playerToSplit != player['name']:
                    groupedTribute = (
                        gameState['playersAlive'][player['name']]
                    )
                    groupedTribute['groupedWith'].remove(playerToSplit)
