from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield (pages.Intro1)
            yield (pages.Intro2)
            yield (pages.Intro3)
            yield (pages.Intro4)
            yield (pages.Intro5)
            yield (pages.Intro6)
            yield (pages.Intro7)
            yield (pages.Examples)
            yield (pages.Example1)
            yield (pages.Example2)
            yield (pages.Example3)
            yield (pages.PracticeIntro)
            yield (pages.PracticeGame, {'practice_contribution': c(10)})
            yield (pages.PracticeResults)
            yield (pages.Quiz)
            yield (pages.Quiz1, {'q1': 1}) # 3
            yield (pages.ReviewGameRules)
            yield (pages.Quiz1, {'q1': 2})
            yield (pages.Quiz2, {'q2': 1 }) #Constants.q2[0]["answer"] = true
            # yield (pages.ReviewGameRules)
            # yield (pages.Quiz2, {'q2': 0 })
            yield (pages.Quiz3, {
                'q3a': 1,
                'q3b': 0
            })
            # yield (pages.ReviewGameRules)
            # yield (pages.Quiz3, { 'q3a': 0, 'q3b': 1, })
            yield (pages.Quiz4, {
                'q4a': 2, # 2 Constants.q4[0]["answer"],
                'q4b': 1, # 1 Constants.q4[1]["answer"],
                'q4c': 2, # 2 Constants.q4[2]["answer"],
                'q4d': 2, # 2 Constants.q4[3]["answer"],
                'q4e': 1, # 1 Constants.q4[4]["answer"],
                'q4f': 2, # 2 Constants.q4[5]["answer"]
            })
            # yield (pages.ReviewGameRules)
            # yield (pages.Quiz4, {
            #     'q4a': 2,
            #     'q4b': 1,
            #     'q4c': 2,
            #     'q4d': 2,
            #     'q4e': 1,
            #     'q4f': 2,
            # })
            yield (pages.GameIntro)
