from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .constants import Constants


class PlayerBot(Bot):
    # def contribution_type():
    #     return 10

    def play_round(self):

        # if self.round_number < 4:
        #     contribute = c(10 - self.round_number)
        #     withhold = c(0 + self.round_number)
        contribute = c(10)
        withhold = c(0)

        yield (pages.Game, {'contributed': contribute, 'withheld': withhold})
        yield (pages.Results)
        if self.round_number == Constants.game_rounds:
            yield (pages.Congrats)
            yield (pages.FinalResults)
