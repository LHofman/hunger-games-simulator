import random
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState

class Sponsors(EventRule):
    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ) -> TextAndTerms:
        text = textAndTerms['text']
        
        if text.find('(Sponsor') == -1: return textAndTerms

        if len(gameState['sponsors']) <= 0:
            return {
                **textAndTerms,
                'text': text.replace('(Sponsor)', 'an unknown sponsor')
            }

        isFixedSponsor = (
            gameState['options'].get('oneSponsorPerTribute', False)
        )
        if (
            not isFixedSponsor or
            len(gameState['sponsors']) != gameState['totalTributes']
        ):
            return {
                **textAndTerms,
                'text': text.replace(
                    '(Sponsor)',
                    random.choice(gameState['sponsors'])
                )
            }

        if text.find('(Sponsor::opposing)') == -1:
            currentTributeSponsor = (
                gameState['sponsors'][gameState['currentTribute']['index'] - 1]
            )
            return {
                **textAndTerms,
                'text': text.replace('(Sponsor)', currentTributeSponsor)
            }

        sponsorIndex = gameState['currentTribute']['index'] - 1
        otherSponsors = (
            gameState['sponsors'][:sponsorIndex] +
            gameState['sponsors'][sponsorIndex+1:]
        )
        return {
            **textAndTerms,
            'text': text.replace(
                '(Sponsor::opposing)',
                random.choice(otherSponsors)
            )
        }
