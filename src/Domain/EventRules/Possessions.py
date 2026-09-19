import random
import re
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import (
    Event,
    GameRoundState,
    GameRoundStateWithoutEvent,
    Tribute
)

class Possessions(EventRule):
    def canPlayEvent(
        self,
        event: Event,
        gameState: GameRoundStateWithoutEvent
    ) -> bool:
        if 'requiresPossessions' not in event: return True

        for possession in event['requiresPossessions']:
            playerHasPossession = self.doesTributeHavePossession(
                gameState['currentTribute'],
                possession['type'],
                possession['value']
            )

            if 'inverse' in possession and possession['inverse']:
                if playerHasPossession: return False
            else:
                if not playerHasPossession: return False

        return True

    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ) -> TextAndTerms:
        text = textAndTerms['text']
        terms = textAndTerms.get('terms', {})

        index = text.find('(Possession:')
        while (index > -1):
            match = re.search(r'\d', text[index:])
            if not match: raise ValueError(
                f'No number found in possession term: {text[index:]}'
            )

            number = int(match.group())
            numberIndex = match.start()

            possessionType = text[
                (index + len('(Possession:')) : (index + numberIndex)
            ]
            possession = random.choice(
                gameState.get('currentTribute')['possessions'][possessionType]
            )
            term = f'(Possession:{possessionType}{number})'
            terms[term] = possession

            text = text.replace(term, possession)

            index = text.find('(Possession:')

        return { **textAndTerms, 'text': text, 'terms': terms }
    
    def handleEventEffects(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ) -> None:
        self.__handleAddPossessions(gameState, textAndTerms)
        self.__handleRemovePossessions(gameState, textAndTerms)

    def __handleAddPossessions(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ):
        event = gameState['event']

        if 'addPossessions' not in event: return

        players = textAndTerms.get('players', [])

        for possession in event['addPossessions']:
            value = possession['value']
            if value in textAndTerms.get('terms', {}):
                value = textAndTerms.get('terms', {})[value]

            playerName = players[possession['player'] - 1]['name']
            tribute = gameState['playersAlive'][playerName]
            possessionType = possession['type']

            if possessionType in tribute['possessions']:
                if possessionType not in (
                    gameState['options']['possessionsWithoutDuplicates']
                ):
                    tribute['possessions'][possessionType].append(value)
            else:
                tribute['possessions'][possessionType] = [value]

    def __handleRemovePossessions(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ):
        event = gameState['event']

        if 'removePossessions' not in event: return

        players = textAndTerms.get('players', [])

        for possession in event['removePossessions']:
            value = possession['value']
            if value in textAndTerms.get('terms', {}):
                value = textAndTerms.get('terms', {})[value]

            playerName = players[possession['player'] - 1]['name']
            tribute = gameState['playersAlive'][playerName]
            possessionType = possession['type']

            if self.doesTributeHavePossession(tribute, possessionType, value):
                tribute['possessions'][possessionType].remove(value)

    @staticmethod
    def doesTributeHavePossession(
        tribute: Tribute,
        type: str,
        value: str
    ) -> bool:
        if value == 'any':
            return (
                type in tribute['possessions'] and
                len(tribute['possessions'][type]) > 0
            )
        else:
            return (
                type in tribute['possessions'] and
                value in tribute['possessions'][type]
            )