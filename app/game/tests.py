from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .constants import Constants


class PlayerBot(Bot):
    # def contribution_type():
    #     return 10
    cases = [
        'avg', # : { 'contribute': c(6), 'withhold': c(4) },
        'min', # : { 'contribute': c(0), 'withhold': c(10) },
        'max', # :{ 'contribute': c(0), 'withhold': c(10) },
        'falling',
        'switch'
    ]

    def play_round(self):
        case = self.case
        if self.case == 'avg':
            contribute= c(6)
            withhold= c(4)
        if self.case == 'max':
            contribute= c(10)
            withhold= c(0)
        if self.case == 'min':
            contribute= c(0)
            withhold= c(10)
        if self.case == 'falling':
            contribute= c(10 - self.round_number)
            withhold= c(self.round_number)
        if self.case == 'switch':
            if self.round_number <= 4:
                contribute= c(10)
                withhold= c(0)
            else:
                contribute= c(0)
                withhold= c(10)

        yield (pages.Game, {'contributed': contribute, 'withheld': withhold})
        yield (pages.Results)
        if self.round_number == Constants.game_rounds:
            yield (pages.Congrats)
            # print(self.html)
            yield (pages.FinalResults)
