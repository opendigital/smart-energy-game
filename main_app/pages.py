from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class ConsentForm(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class GameFraming(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class GameStructure1(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class GameStructure2(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class GameOutcomes1(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class GameOutcomes2(Page):
    # Displayed only in the first round
    def is_displayed(self):
        return self.player.round_number == 1


class Survey(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return {'months': ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'],
                'index': self.group.round_number - 1,
                'months_number':[1,2,3,4,5,6,7,8,9,10,11,12]}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {'months': ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'],
                'index': self.group.round_number - 1,
                'months_number':[1,2,3,4,5,6,7,8,9,10,11,12]}

    def before_next_page(self):
        if self.group.all_rounds_contribution() >= Constants.group_goal and self.round_number == 12:
            for p in self.group.get_players():
                p.payoff += self.group.bonus



class Congrats(Page):
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['question']

    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def question_choices(self):
        choices = ['Adam', 'March', 'June', 'July']
        random.shuffle(choices)
        return choices


page_sequence = [
    ConsentForm,
    GameFraming,
    GameStructure1,
    GameStructure2,
    GameOutcomes1,
    GameOutcomes2,
    Survey,
    ResultsWaitPage,
    Results,
    Congrats,
    PostSurvey
]
