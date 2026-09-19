import random
import re
from Domain.EventRule import EventRule, TextAndTerms
from Domain.types import GameRoundState

class OtherTerms(EventRule):
  def replaceTextTerms(self, gameState: GameRoundState, textAndTerms: TextAndTerms) -> TextAndTerms:
    text = textAndTerms['text']
    terms = textAndTerms.get('terms', {})

    for (key, values) in gameState.get('otherTerms').items():
      index = text.find('(%s' % key)
      while (index > -1):
        match = re.search(r'\d', text[index:])
        if (not match): raise Exception('No number found in other term: %s' % text[index:])

        number = int(match.group())
        term = '(%s%d)' % (key, number)

        value = random.choice(values)
        terms[term] = value

        text = text.replace(term, value)

        index = text.find('(%s' % key)

    return { **textAndTerms, 'text': text, 'terms': terms }
