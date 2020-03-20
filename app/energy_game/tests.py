from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number < 4:
            contribute = c(10)
            withhold = c(0)
        if self.round_number >= 4:
            contribute = c(5)
            withhold = c(5)

        yield (pages.Game, {'contributed': contribute, 'withheld': withhold})
        yield (pages.Results)
