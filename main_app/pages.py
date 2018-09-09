from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class WaitingRoom(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    def is_displayed(self):
        return self.round_number == 1


class ConsentForm(Page):
    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Consent'}


class GameFraming(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameStructure1(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.repeatQuiz1

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction1+=1

class GameStructure2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameOutcomes1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameOutcomes2(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.repeatQuiz2

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction2+=1


class ExamplesTransition(Page):
    def is_displayed(self):
        return self.player.display_instructions()

    def vars_for_template(self):
        return {'progress': 'Examples'}


class ExamplesOne(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class ExamplesTwo(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class ExamplesThree(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class PracticeTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Practice'}


class PracticeGame(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2,
                'progress': 'Practice'}

    def before_next_page(self):
        self.player.private_contribution = c(10) - self.player.contribution
        self.player.random_others_contribution = c(0)
        for i in range(0, Constants.players_per_group):
            self.player.random_others_contribution += c(random.randint(0,11))
        self.player.group_random_total_contribution = self.player.contribution + self.player.random_others_contribution


class PracticeResults(Page):
    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds/2,
                'progress': 'Practice'}


class QuizTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Quiz'}


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['equilibrium_tokens']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[0]}

    def is_displayed(self):
        return self.round_number == 1 and self.player.repeatQuiz1

    def equilibrium_tokens_choices(self):
        choices = ["2 tokens", "3 tokens", "6 tokens", "10 tokens"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.is_equilibrium_tokens_correct():
            self.player.repeatQuiz1 = False
        else:
            self.player.repeatQuiz1 = True


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['donation']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[1]}

    def is_displayed(self):
        return self.round_number == 1 and self.player.repeatQuiz2

    def donation_choices(self):
        choices = ["True","False"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.is_donation_correct():
            self.player.repeatQuiz2 = False
        else:
            self.player.repeatQuiz2 = True


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['max_individual', 'max_group']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

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

    def before_next_page(self):
        self.player.is_max_individual_correct()
        self.player.is_max_group_correct()


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['bonus_question']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def bonus_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif value/10 > 0.72:
            return 'Round the value up to two decimals'

    def before_next_page(self):
        self.player.is_bonus_question_correct()


class Quiz5(Page):
    form_model = 'player'
    form_fields = ['tokens_question']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def tokens_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif (value / 10) > 0.72:
            return 'Round the value up to two decimals'

    def before_next_page(self):
        self.player.is_tokens_question_correct()


class Quiz6(Page):
    form_model = 'player'
    form_fields = ['expected_contribution', 'expected_individual']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds/2

    def error_message(self, values):
        if values["expected_contribution"] + values["expected_individual"] != 120:
            return 'The numbers must add up to 120'

    def before_next_page(self):
        self.player.check_answers()


class Survey(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2,
                'progress': 'Game'}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds/2,
                'progress': 'Game'}


class Congrats(Page):
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds/2 or self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2,
                'progress': 'Game'}


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['birth', 'gender', 'ethnic_group', 'economic_status', 'previous_experiments', 'reliability']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


class FinalResults(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    #WaitingRoom,
    #ConsentForm,
    #GameFraming,
    #GameStructure1,
    #GameStructure2,
    #GameOutcomes1,
    #GameOutcomes2,
    #ExamplesTransition,
    #ExamplesOne,
    ExamplesTwo,
    ExamplesThree,
    #PracticeTransition,
    #PracticeGame,
    #PracticeResults,
    #QuizTransition,
    #Quiz1,
    #GameStructure1,
    #Quiz1,
    #Quiz2,
    #GameOutcomes2,
    #Quiz2,
    Quiz3,
    ExamplesTwo,
    ExamplesThree,
    Quiz3,
    #ExamplesThree,
    #ExamplesTwo,
    #Quiz3,
    #Quiz4,
    #ExamplesOne,
    #Quiz4,
    #Quiz5,
    #Quiz5,
    #Quiz6,
    #Quiz6,
    #Survey,
    #ResultsWaitPage,
    #Results,
    #Congrats,
    #FinalResults,
    #PostSurvey
]
