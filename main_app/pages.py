from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class WaitingRoom(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class ConsentForm(Page):
    def is_displayed(self):
        return self.player.round_number == 1


class GameFraming(Page):
    def is_displayed(self):
        return (self.player.round_number == 1 or self.player.round_number == Constants.num_rounds/2+1) and not self.player.everything_correct


class GameStructure1(Page):
    def is_displayed(self):
        return (self.player.round_number == 1 or self.player.round_number == Constants.num_rounds/2+1) and not self.player.everything_correct


class GameStructure2(Page):
    def is_displayed(self):
        return (self.player.round_number == 1 or self.player.round_number == Constants.num_rounds/2+1) and not self.player.everything_correct


class GameOutcomes1(Page):
    def is_displayed(self):
        return (self.player.round_number == 1 or self.player.round_number == Constants.num_rounds/2+1) and not self.player.everything_correct


class GameOutcomes2(Page):
    def is_displayed(self):
        return (self.player.round_number == 1 or self.player.round_number == Constants.num_rounds/2+1) and not self.player.everything_correct


class Survey(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds/2}


class Congrats(Page):
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds/2 or self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2}


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['equilibrium_tokens']

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def equilibrium_tokens_choices(self):
        choices = ["2 tokens", "3 tokens", "6 tokens", "10 tokens"]
        random.shuffle(choices)
        return choices


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['donation']

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def donation_choices(self):
        choices = ["The total tokens in the House Conservation Fund x $.01 to convert the energy tokens into dollars.",
                "2x the total tokens in the House Conservation Fund x $.01 to convert the energy tokens into dollars ",
                "3x the total tokens in the House Conservation Fund x $.01 to convert the energy tokens into dollars "]
        random.shuffle(choices)
        return choices


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['max_individual', 'max_group']

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def max_individual_choices(self):
        choices = ["0 tokens", "3 tokens", "6 tokens", "10 tokens"]
        random.shuffle(choices)
        return choices

    def max_group_choices(self):
        choices = ["0 tokens", "3 tokens", "6 tokens", "10 tokens"]
        random.shuffle(choices)
        return choices


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['bonus_question']

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def bonus_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif value/10 > 0.72:
            return 'Round the value up to two decimals'


class Quiz5(Page):
    form_model = 'player'
    form_fields = ['tokens_question']

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def tokens_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif (value / 10) > 0.72:
            return 'Round the value up to two decimals'


class Quiz6(Page):
    form_model = 'player'
    form_fields = ['expected_contribution', 'expected_individual']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds/2

    def error_message(self, values):
        if values["expected_contribution"] + values["expected_individual"] != 120:
            return 'The numbers must add up to 120'

    def before_next_page(self):
        self.player.check_answers()


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['birth', 'gender', 'ethnic_group', 'economic_status', 'previous_experiments', 'reliability']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


class FinalResults(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    WaitingRoom,
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
    Quiz1,
    Quiz2,
    Quiz3,
    Quiz4,
    Quiz5,
    Quiz6,
    FinalResults,
    PostSurvey
]
