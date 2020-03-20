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
            yield (pages.Quiz1, {'q1': 1})

            yield (pages.Quiz2, {'q2': 0 }) #Constants.q2[0]["answer"] = False
            yield (pages.ReviewGameRules)
            yield (pages.Quiz2, {'q2': 0 })

            # Constants.q3[0]["answer"]
            yield (pages.Quiz3, { 'q3a': 0, 'q3b': 1, })
            yield (pages.ReviewGameRules)
            yield (pages.Quiz3, { 'q3a': 0, 'q3b': 1, })

            yield (pages.Quiz4, {
                'q4a': 3, # 2 Constants.q4[0]["answer"],
                'q4b': 3, # 1 Constants.q4[1]["answer"],
                'q4c': 3, # 2 Constants.q4[2]["answer"],
                'q4d': 3, # 2 Constants.q4[3]["answer"],
                'q4e': 3, # 1 Constants.q4[4]["answer"],
                'q4f': 3, # 2 Constants.q4[5]["answer"]
            })

            yield (pages.ReviewGameRules)
            yield (pages.Quiz4, {
                'q4a': 3,
                'q4b': 3,
                'q4c': 3,
                'q4d': 3,
                'q4e': 3,
                'q4f': 3
            })
