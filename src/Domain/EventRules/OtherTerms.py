import random
import re
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState


class OtherTerms(EventRule):
    def replaceTextTerms(
        self,
        gameState: GameRoundState,
        textAndTerms: TextAndTerms
    ) -> TextAndTerms:
        text = textAndTerms['text']
        terms = textAndTerms.get('terms', {})

        for (key, values) in gameState.get('otherTerms').items():
            index = text.find(f'({key}')
            while (index > -1):
                match = re.search(r'\d', text[index:])
                if not match: raise ValueError(
                    f'No number found in other term: {text[index:]}'
                )

                number = int(match.group())
                term = f'({key}{number})'

                value = random.choice(values)
                terms[term] = value

                text = text.replace(term, value)

                index = text.find(f'({key}')

        return { **textAndTerms, 'text': text, 'terms': terms }
