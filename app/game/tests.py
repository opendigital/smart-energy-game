from otree.api import Currency as c, currency_range
import os
from . import pages
from ._builtin import Bot
from .constants import Constants


class PlayerBot(Bot):
    # def contribution_type():
    #     return 10
    cases = [
        # 'avg', # : { 'contribute': c(6), 'withhold': c(4) },
        # 'min', # : { 'contribute': c(0), 'withhold': c(10) },
        # 'max', # :{ 'contribute': c(0), 'withhold': c(10) },
        # 'falling',
        # 'increasing',
        'winning'
    ]

    def dump_html(self,_html):
        if Constants.TESTS_EXPORT_HTML:
            print("\n\n\n")
            print("<article>")
            print(_html)
            print("</article>")
            print("\n\n\n")
            print("<hr />\n\n\n")

    def print_round_title(self, title_text):
        print("\n[CASE: ", title_text, "]")

    def play_round(self):
        case = self.case
        round_title = "default"
        if self.case == 'avg':
            round_title = "AVG"
            contribute= c(6)
            withhold= c(4)
        if self.case == 'max':
            round_title = "MAX"
            contribute= c(10)
            withhold= c(0)
        if self.case == 'min':
            round_title = "MIN"
            contribute= c(0)
            withhold= c(10)
        if self.case == 'falling':
            round_title = "FALLING"
            contribute= c(10 - self.round_number)
            withhold= c(self.round_number)
        if self.case == 'increasing':
            round_title = "increasing"
            contribute= c(0 + ((self.round_number-1) * 2))
            withhold= c(10 - ((self.round_number-1) * 2))
        if self.case == 'winning':
            round_title = "WINNING"
            if self.round_number == 1:
                contribute= c(5)
            elif self.round_number == 2:
                contribute= c(7)
            elif self.round_number == 3:
                contribute= c(6)
            elif self.round_number == 4:
                contribute= c(4)
            elif self.round_number == 5:
                contribute= c(0)
            else:
                contribute= c(0)

        # print('round', self.round_number)
        if self.round_number == 1:
            self.print_round_title(round_title)
            #     print(os.environ)
            # self.dump_html(self.html)
        if self.round_number <= Constants.game_rounds:
            yield (pages.Game, {'contributed': contribute, 'withheld': (10-contribute)})
            self.dump_html(self.html)
            yield (pages.Results)
            self.dump_html(self.html)
        if self.round_number == Constants.num_rounds:
            yield (pages.Congrats)
            self.dump_html(self.html)
            yield (pages.FinalResults)
            # self.dump_html(self.html)
