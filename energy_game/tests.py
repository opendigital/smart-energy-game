from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        #yield (pages.WaitingRoom)
        if self.round_number == 1:
            yield (pages.IntroConsent)
            yield (pages.IntroOutline,)
            yield (pages.IntroIntroduction,)
            yield (pages.IntroStructure,)
            yield (pages.IntroGameplay,)
            yield (pages.IntroFinancialOutcomes,)
            yield (pages.IntroEnvironOutcomes,)
            yield (pages.Examples,)
            yield (pages.Example1,)
            yield (pages.Example2,)
            yield (pages.Example3,)
            yield (pages.PracticeIntro,)
            yield (pages.PracticeGame, {'contribution': c(10)})
            yield (pages.PracticeResults,)
        if self.round_number == 2:
            yield (pages.PracticeGame, {'contribution': c(10)})
            yield (pages.PracticeResults,)
            yield (pages.Quiz,)
            yield (pages.Quiz1, {'quiz_1': Constants.answers[0]})
            yield (pages.Quiz2, {'quiz_2': Constants.answers[1]})
            yield (pages.Quiz3, {
                'Q3a': Constants.answers[2],
                'Q3b': Constants.answers[3]
            })
            yield (pages.Quiz4, {
                'answerQ4a1': Constants.answers[4],
                'answerQ4a2': Constants.answers[5],
                'answerQ4a3': Constants.answers[6],
                'answerQ4b1': Constants.answers[7],
                'answerQ4b2': Constants.answers[8],
                'answerQ4b3': Constants.answers[9]
            })
            yield (pages.RealGameTransition,)
        if self.round_number >= 2:
            yield (pages.Survey,{
                'contribution':c(5),
                'private_contribution':c(5)
            })
            yield (pages.Results,)
            if self.round_number == 13:
                yield (pages.FinalResults,)
        #yield (pages.PostSurvey)
