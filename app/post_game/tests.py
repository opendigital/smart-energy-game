from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.PostSurvey1, {
             's1a1': 'test',
             's1a2': True,
             's1a3': 'test',
             's1a4': 'test',
             's1a5': 'test',
             's1b1': 1,
             's1b2': 1,
             's1b3': 1,
             's1b4': 1,
             's1b5': 1,
             's1c1': 1,
             's1c2': 1,
             's1c3': 1,
             's1c4': 1,
             's1c5': 1,
        })
        yield (pages.PostSurvey2, {
            's2a0': 1,
            's2a1': 1,
            's2a2': 1,
            's2a3': 1,
            's2a4': 1,
            's2a5': 1,
            's2a6': 1,
            's2a7': 1,
            's2a8': 1,
        })
        yield (pages.PostSurvey3, {
            's3a0':1,
            's3a1':1,
            's3a2':1,
            's3a3':1,
            's3a4':1,
            's3a5':1,
            's3a6':1,
            's3a7':1,
            's3a8':1,
            's3a9':1,
            's3a10':1 ,
        })
        yield (pages.PostSurvey4, {
            's4a1': 1901,
            's4a2': 1,
            's4a3': 1,
            's4a4': 1,
            's4a5': 1,
            's4a6': True,
            's4a7': 1,
            's4a8': 1,
        })
        yield (pages.Debriefing, {
            'survey_consent': True
        })
