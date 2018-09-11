from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class WaitingRoom(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    #group_by_arrival_time = True

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
        return (self.round_number == 1 and self.player.timesInstruction1 == 0) or (self.round_number == 2 and self.player.repeatQuiz1)

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction1 += 1


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
        return (self.round_number == 1 and self.player.timesInstruction2 == 0) or (
                self.round_number == 2 and self.player.repeatQuiz2)

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction2 += 1


class ExamplesTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class ExamplesOne(Page):
    def is_displayed(self):
        return(self.round_number == 1 and self.player.timesInstruction4 == 0) or (
                self.round_number == 2 and self.player.repeatQuiz4)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction4 += 1


class ExamplesTwo(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3a == 0) or (
                self.round_number == 2 and self.player.repeatQuiz3a)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction3a += 1


class ExamplesThree(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3b == 0) or (
                self.round_number == 2 and self.player.repeatQuiz3b)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction3b += 1


class PracticeTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Practice'}


class PracticeGame(Page):
    form_model = 'player'
    form_fields = ['practice_contribution']

    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2,
                'progress': 'Practice'}

    def before_next_page(self):
        self.player.practice_private_contribution = c(10) - self.player.practice_contribution
        self.player.random_others_contribution = c(0)
        for i in range(0, Constants.players_per_group):
            self.player.random_others_contribution += c(random.randint(0,11))
        self.player.group_random_total_contribution = self.player.practice_contribution + self.player.random_others_contribution


class PracticeResults(Page):
    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds/2,
                'progress': 'Practice'}


class QuizTransition(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return {'progress': 'Quiz'}


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['Q1']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[0],
                'xINST':self.player.timesInstruction1,
                'REP?':self.player.repeatQuiz1}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction1 <= 1 and not self.player.is_equilibrium_tokens_correct()

    def Q1_choices(self):
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
    form_fields = ['Q2']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[1]}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction1 <= 1 and not self.player.is_donation_correct()

    def Q2_choices(self):
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
    form_fields = ['Q3a', 'Q3b']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': 'True',
                'correct_answer2': 'True',
                }

    def is_displayed(self):
        return self.round_number == 2 and (self.player.timesInstruction3a <= 1 or self.player.timesInstruction3b <= 1) and not self.player.is_both_Examples_right()

    def Q3a_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def Q3b_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.is_both_Examples_right():
            self.player.repeatQuiz3a = False
            self.player.repeatQuiz3b = False
        else:
            if self.player.is_max_individual_correct():
                self.player.repeatQuiz3a = False
            else:
                self.player.repeatQuiz3a = True

            if self.player.is_max_group_correct():
                self.player.repeatQuiz3b = False
            else:
                self.player.repeatQuiz3b = True


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['answerQ4a1','answerQ4a2','answerQ4a3',
                   'answerQ4b1','answerQ4b2','answerQ4b3']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer':'$1.08','correct_answer2':'$1.00','correct_answer3':'$2.08',
                'correct_answer4':'$1.08','correct_answer5':'$0.00','correct_answer6':'$1.08'}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction4 <= 1 and not self.player.is_all_values_right()

    def bonus_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif value/10 > 0.72:
            return 'Round the value up to two decimals'

    def before_next_page(self):
        if self.player.is_all_values_right():
            self.player.repeatQuiz4 = False
        else:
            self.player.repeatQuiz4 = True


class RealGameTransition(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return {'progress': 'Game'}

"""
class RealGameTransition(Page):
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
"""


class Survey(Page):
    form_model = 'player'
    form_fields = ['contribution','private_contribution']

    def is_displayed(self):
        return self.round_number >= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    def is_displayed(self):
        return self.round_number >= 2

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.round_number >= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class Congrats(Page):
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['birth', 'gender', 'ethnic_group', 'economic_status', 'previous_experiments', 'reliability']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class FinalResults(Page):
    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game',
                'goal_meet': Constants.group_goal <= self.group.all_rounds_contribution()}

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    ConsentForm,
    WaitingRoom,
    GameFraming,
    GameStructure1,
    GameStructure2,
    GameOutcomes1,
    GameOutcomes2,
    ExamplesTransition,
    ExamplesOne,
    ExamplesTwo,
    ExamplesThree,
    PracticeTransition,
    PracticeGame,
    PracticeResults,
    QuizTransition,
    Quiz1,
    GameStructure1,
    Quiz1,
    Quiz2,
    GameOutcomes2,
    Quiz2,
    Quiz3,
    ExamplesTwo,
    ExamplesThree,
    Quiz3,
    Quiz4,
    ExamplesOne,
    Quiz4,
    RealGameTransition,
    Survey,
    ResultsWaitPage,
    Results,
    FinalResults,
    #PostSurvey
]
