import random
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    def is_displayed(self):
        print('self.round_number', self.round_number)
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Consent'}


class Results(Page):
    def vars_for_template(self):
        return {'progress': 'Consent'}




class IntroConsent(Page):
    """Introduction: Consent Form"""
    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Consent'}


class IntroOutline(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class IntroOverview(Page):
    def is_displayed(self):
        return (self.round_number == 1 \
            and self.player.page_attempts == 0) \
            or (self.round_number == 2 \
            and self.player.repeatQuiz1)


    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'reduction_goal': Constants.reduction_goal,
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
        }

    def before_next_page(self):
        self.player.page_attempts += 1


class IntroStructure(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'reduction_goal': Constants.reduction_goal,
            'optimal_contribution': '6',
            'game_tokens': Constants.game_tokens,
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'token_goal': Constants.game_goal,
            'token_value': Constants.token_value,
        }



class IntroGameplay(Page):
    def is_displayed(self):
        return (self.round_number == 1)


    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_value': Constants.token_value,
        }



class IntroFinancialOutcomes(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return  {
            'progress': 'Introduction',
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_goal': Constants.token_goal,
            'token_value': Constants.token_value,
            'game_tokens': Constants.token_goal,
        }


class IntroEnvironOutcomes(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return  {
            'progress': 'Introduction',
            'game_players': '25',
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_value': Constants.token_value,
        }


    # def before_next_page(self):
    #     self.player.page_attempts += 1


class Examples(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class Example1(Page):
    def is_displayed(self):
        return(self.round_number == 1)

    def vars_for_template(self):
        return {
            'progress': 'Examples',
            'game_goal': '60',
            'classes': {
                'row1': 'badge-success',
                'row2': 'hide',
                'row3': 'hide',
                'row4': 'hide',
                'row5': 'hide',
            }
        }

    # def before_next_page(self):
    #     self.player.timesInstruction4 += 1


class Example2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'badge-danger',
                'row3': 'badge-success',
                'row4': 'hide',
                'row5': 'hide',
            }
        }

    # def before_next_page(self):
    #     self.player.timesInstruction3a += 1


class Example3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': 'badge-success',
                'row5': 'badge-danger',
            }
        }



class PracticeIntro(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Practice'}




class PracticeGame(Page):
    form_model = 'player'
    form_fields = [
        'practice_contribution'
    ]

    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        return {
            'progress': 'Practice',
            'current_month': Constants.MONTHS[(self.round_number - 1) % 12],
            'current_round': self.round_number % 12,
        }

    def before_next_page(self):
        self.player.practice_private_contribution = \
            c(10) - self.player.practice_contribution

        self.player.random_others_contribution = c(0)

        for i in range(0, 24):
            self.player.random_others_contribution += c(random.randint(0, 11))

        self.player.group_random_total_contribution = \
            self.player.practice_contribution + \
            self.player.random_others_contribution




class PracticeResults(Page):
    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        return {
            'progress': 'Practice',
            'current_month': Constants.MONTHS[(self.round_number - 1) % 12],
            'current_round': self.round_number % 12,
        }


class Quiz(Page):
    after_all_players_arrive = 'init_attempts'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Quiz'}


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1']

    def is_displayed(self):
        print('self.session.vars', self.session.vars)
        print('self.player', self.player.participant.vars)

        return self.round_number == 1 \
            and self.player.q1_attempts <= Constants.quiz_max_attempts \
            and not self.player.q1_correct


    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'q1_attempts': self.player.q1_attempts,
            'q1_correct': self.player.q1_correct,
            'show_hint': self.player.q1_attempts > Constants.quiz_max_attempts,
            'quiz_hint': Constants.quiz_default_hint,
            "answer_key": dict(q1=Constants.q1[0]["answer"])
        }

    def q1_choices(self):
        choices = Constants.q1[0]["choices"]
        random.shuffle(choices)
        return choices

    def error_message(self, values):
        valid = self.player.valid_q1(values)
        if not valid:
            self.session.vars["quizdata"] = 'change'
            return 'errors'

    def before_next_page(self):
        print(self.session.vars["quizdata"])
        self.session.vars["quizdata"] = 'change'




class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']

    def vars_for_template(self):
        print('self.session.vars', self.session.vars)
        print('self.player')
        return {
            'progress': 'Quiz',
            'show_hint': self.player.q2_attempts > Constants.quiz_max_attempts,
            'q2_attempts': self.player.q2_attempts,
            'q2_correct': self.player.q2_correct,
            'quiz_hint': Constants.quiz_default_hint,
            'answer_key': dict(q2=Constants.q2[0]["answer"]),
        }

    def is_displayed(self):
        return self.round_number == 1 \
            and self.player.q2_attempts <= Constants.quiz_max_attempts \
            and not self.player.q2_correct

    def q2_choices(self):
        choices = Constants.q2[0]["choices"]
        random.shuffle(choices)
        return choices

    def error_message(self, values):
        valid = self.player.valid_q2(values)
        if not valid:
            self.player.review_rules = 2
            return 'errors'

        self.player.review_rules = 0

    def before_next_page(self):
        print(self.session.vars["quizdata"])
        self.session.vars["quizd2222"] = 'olddata'
        self.session.vars["quizdata3"] = 'newvalue'





class Quiz3(Page):
    form_model = 'player'
    form_fields = [
        'q3a',
        'q3b',
    ]

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'show_hint': self.player.q3a_attempts > 2 or self.player.q3b_attempts > 2,
            'answer_key': dict(
                q3a=Constants.q3[0]["answer"],
                q3b=Constants.q3[1]["answer"],
            ),
            'q3a_attempts': self.player.q3a_attempts,
            'q3b_attempts': self.player.q3b_attempts,
            'q3_hint': [
                Constants.q3[0]["hint"],
                Constants.q3[1]["hint"],
            ]
        }


    def is_displayed(self):
        return self.round_number == 1 \
            and (self.player.q3a_attempts <= Constants.quiz_max_attempts) \
            and (self.player.q3a_attempts <= Constants.quiz_max_attempts) \
            and not self.player.q3a_correct \
            and not self.player.q3b_correct

    def q3a_choices(self):
        choices1 = Constants.q3[0]["choices"]
        random.shuffle(choices1)
        return choices1

    def q3b_choices(self):
        choices2 = Constants.q3[1]["choices"],
        random.shuffle(choices2)
        return choices2

    def error_message(self, values):
        valid = self.player.valid_q3(values)
        if not valid:
            self.player.review_rules = 2
            return 'errors'
        else:
            self.player.review_rules = 0


    # def before_next_page(self):
        # if self.player.valid_q3():
        #     self.player.page_attempts = 0
        # else:
        #     self.player.page_attempts = 1




class Quiz4(Page):
    form_fields = [
        'quiz_4a1',
        'quiz_4a2',
        'quiz_4a3',
        'quiz_4b1',
        'quiz_4b2',
        'quiz_4b3'
    ]

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'correct_answer': '$1.00',
            'correct_answer2': '$16.00',
            'correct_answer3': '$17.00',
            'correct_answer4': '$1.00',
            'correct_answer5': '$0.00',
            'correct_answer6': '$1.00'
        }

    def is_displayed(self):
        return self.round_number == 1
        # return self.round_number == 2 \
            # and self.player.timesInstruction4 <= 1 \
            # and not self.player.is_all_values_right()

    # def before_next_page(self):
    #     if self.player.is_all_values_right():
    #         self.player.repeatQuiz4 = False
    #     else:
    #         self.player.repeatQuiz4 = True




class ReviewGameRules(Page):
    template_name = 'onboarding_app/Example3.html'

    def is_displayed(self):
        if self.round_number > 1:
            return False

        if self.player.review_rules <= 0:
            return False
        elif self.player.review_rules == 1:
            template_name = 'onboarding_app/IntroEnvironOutcomes.html'
            return True
        elif self.player.review_rules == 2 or self.player.review_rules == 23:
            template_name = 'onboarding_app/Example2.html'
            return True
        elif self.player.review_rules == 3 or self.player.review_rules == 23:
            template_name = 'onboarding_app/Example3.html'
            return True
        elif self.player.review_rules == 4:
            template_name = 'onboarding_app/Example1.html'
            return True
        else:
            return False

    def vars_for_template(self):
        return {
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': 'badge-success',
                'row5': 'badge-danger',
            }
        }

    def before_next_page(self):
        self.player.review_rules = 0




page_sequence = [
    MyPage,
    IntroConsent,
    IntroOutline,
    IntroOverview,
    IntroStructure,
    IntroGameplay,
    IntroFinancialOutcomes,
    IntroEnvironOutcomes,
    Examples,
    Example1,
    Example2,
    Example3,
    PracticeIntro,
    PracticeGame,
    PracticeResults,
    # QUIZ
    Quiz,
    Quiz1,     # Q1
    Quiz2,     # Q2
    ReviewGameRules, # IntroEnvironOutcomes,
    Quiz2,
    Quiz3,     # Q3
    ReviewGameRules, # Example2,
    ReviewGameRules, # Example3,
    Quiz3,
    Quiz4,     # Q4
    ReviewGameRules, # Example1,
    Quiz4,
]
