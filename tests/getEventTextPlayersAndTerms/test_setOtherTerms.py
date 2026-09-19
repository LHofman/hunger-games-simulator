import pytest
from pytest_mock import MockerFixture
from Domain.EventRules.OtherTerms import OtherTerms
from Domain.EventRule import TextAndTerms
from Domain.types import GameRoundState
from tests.defaults import (
  defaultGameRoundState,
)

@pytest.fixture(autouse=True)
def test_mock(mocker: MockerFixture):
  mocker.patch(
    'random.choice',
    side_effect=lambda list: list[0] # type: ignore
  )

def test_setOtherTerms():
  gameState: GameRoundState = {
    **defaultGameRoundState,
    'otherTerms': { 'Animal': ['cat', 'dog'] }
  }

  textAndTerms: TextAndTerms = {
    'text': 'Tribute finds a (Animal1), They pet it and the (Animal1) follows them around',
  }

  result = OtherTerms().replaceTextTerms(
    gameState,
    textAndTerms,
  )

  assert result == {
    'text': 'Tribute finds a cat, They pet it and the cat follows them around',
    'terms': { '(Animal1)': 'cat' }
  }