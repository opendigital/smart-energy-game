import random
from otree.api import Currency as c
from otree.api import currency_range
from main_app import models
from ._builtin import Page, WaitPage
from .constants import Constants

class IntroConsent(Page):
    """Introduction: Consent Form"""
    def is_displayed(self):
        return self.player.round_number == 1

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'Consent'}


class IntroOutline(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'Introduction'}


class IntroIntroduction(Page):
    """Page Docstring"""
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
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1



class IntroGameplay(Page):
    """Page Docstring"""
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction2 == 0) \
            or (self.round_number == 2 and self.player.repeatQuiz2)

    """template variables"""
    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'game_players': '25',
            'game_tokens': Constants.game_tokens,
            'optimal_contribution': '6',
            'reduction_goal': '60',
            'game_rounds': Constants.game_rounds,
            'token_value': '.01'
        }

    def before_next_page(self):
        self.player.timesInstruction2 += 1


class IntroFinancialOutcomes(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1

    """template variables"""
    def vars_for_template(self):
        return  {
            'progress': 'Introduction',
            'game_players': '25',
            'optimal_contribution': '6',
            'reduction_goal': '60',
            'game_tokens': Constants.game_tokens,
            'game_rounds': Constants.game_rounds,
            'token_goal': Constants.game_goal,
            'token_value': '.01'
        }


class IntroEnvironOutcomes(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1

    # def is_displayed(self):
    #     return (self.round_number == 1 and self.player.page_attempts == 0) \
    #         or (self.round_number == 2 and self.player.repeatQuiz2)

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.page_attempts += 1


class Examples(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'Examples'}


class Example1(Page):
    """Page Docstring"""
    def is_displayed(self):
        return(self.round_number == 1 and self.player.timesInstruction4 == 0) \
            or (self.round_number == 2 and self.player.repeatQuiz4)

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

    def before_next_page(self):
        self.player.timesInstruction4 += 1


class Example2(Page):
    """Page Docstring"""
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3a == 0) \
            or (self.round_number == 2 and self.player.repeatQuiz3a)

    """template variables"""
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

    def before_next_page(self):
        self.player.timesInstruction3a += 1


class Example3(Page):
    """Page Docstring"""
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3b == 0) \
            or (self.round_number == 2 and self.player.repeatQuiz3b)

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
            self.player.timesInstruction3b += 1


class PracticeIntro(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 1

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'Practice'}


class PracticeGame(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'practice_contribution'
    ]

    def is_displayed(self):
        return self.round_number <= 2

    """template variables""",
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 1) % 12],
            'current_round': self.round_number % 12,
            'is_trial': self.round_number <= Constants.num_rounds / 2,
            'progress': 'Practice'
        }

    def before_next_page(self):
        self.player.practice_private_contribution = \
            c(10) - self.player.practice_contribution

        self.player.random_others_contribution = c(0)

        for i in range(0, 24):
            self.player.random_others_contribution += c(random.randint(0, 11))

        self.player.group_random_total_contribution = \
            self.player.practice_contribution + self.player.random_others_contribution


class PracticeResults(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number <= 2

    """template variables"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 1) % 12],
            'current_round': self.round_number % 12,
            'is_trial': self.round_number <= Constants.num_rounds / 2,
            'progress': 'Practice'
        }


class Quiz(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return {'progress': 'Quiz'}


class Quiz1(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = ['quiz_1']

    def is_displayed(self):
        return self.round_number == 2 \
            and self.player.q1_attempts <= 3 \
            and not self.player.q1_correct

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'q1_attempts': self.player.q1_attempts,
            'q1_correct': self.player.q1_correct,
            'show_hint': self.player.q1_attempts > 2,
            'quiz_hint': Constants.quiz_default_hint,
            'answer_key': [Constants.q1[0]["answer"]],
        }

    # def error_message(self, values):
    #     errors = self.player.validate_q1(values)
    #     return False


class Quiz2(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = ['quiz_2']

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'q2_attempts': self.player.q2_attempts,
            'q2_correct': self.player.q2_correct,
            'show_hint': self.player.q2_attempts > 3,
            'answer_key': [Constants.q2[0]["answer"]],
        }

    def is_displayed(self):
        return self.round_number == 2 \
            and self.player.page_attempts <= 5 \
            and not self.player.q2_correct

    def quiz_2_choices(self):
        choices = [
            "True",
            "False"
        ]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.validate_q2():
            self.player.page_attempts = 0
        else:
            self.player.page_attempts = 1


class Quiz3(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'quiz_3a',
        'quiz_3b'
    ]

    def vars_for_template(self):
        print('q3', Constants.q3)
        return {
            'progress': 'Quiz',
            'correct_answer': 'True',
            'correct_answer2': 'True',
            'show_hint': self.player.q3_attempts > 3,
            'answer_key': [
                Constants.q3[0]["answer"],
                Constants.q3[1]["answer"]
            ],
            'q3_attempts': self.player.q3_attempts,
            'q3a_correct': self.player.q3a_correct,
            'q3b_correct': self.player.q3b_correct,
            'q3a_hint': Constants.quiz_default_hint,
            'q3b_hint': Constants.quiz_default_hint,
        }

    def is_displayed(self):
        return self.round_number == 2 \
            and (self.player.page_attempts <= 1) \
            and not self.player.validate_q3()

    def quiz_3a_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def quiz_3b_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.validate_q2():
            self.player.page_attempts = 0
        else:
            self.player.page_attempts = 1



class Quiz4(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'quiz_4a1',
        'quiz_4a2',
        'quiz_4a3',
        'quiz_4b1',
        'quiz_4b2',
        'quiz_4b3'
    ]

    """template variables"""
    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'xINSTRUCTIONS': self.player.timesInstruction4,
            'correct_answer': '$1.00',
            'correct_answer2': '$16.00',
            'correct_answer3': '$17.00',
            'correct_answer4': '$1.00',
            'correct_answer5': '$0.00',
            'correct_answer6': '$1.00'
        }

    def is_displayed(self):
        return self.round_number == 2 \
            and self.player.timesInstruction4 <= 1 \
            and not self.player.is_all_values_right()

    def before_next_page(self):
        if self.player.is_all_values_right():
            self.player.repeatQuiz4 = False
        else:
            self.player.repeatQuiz4 = True




class Game(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'contribution',
        'private_contribution'
    ]

    def is_displayed(self):
        return self.round_number >= 2

    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game'
        }


class ResultsWaitPage(WaitPage):
    """Page Docstring"""
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    # models.Player.bot_contributions =\
    #    [[10 for x in round_] for round_ in models.Player.bot_contributions]
    # print(models.Player.bot_contributions)

    def is_displayed(self):
        return self.round_number >= 2

    # def before_next_page(self):
    #     self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
    #     print("test")

    # self.models.player.bot_contributions =\
    #   [[10 for x in round_] for round_ in self.player.bot_contributions]
    # print(self.models.group.bot_contributions)

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.set_bots()



class Results(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.round_number >= 2

    # def before_next_page(self):
    #     self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
    #     print("test")

    """template variables"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game'
        }


class Congrats(Page):
    """Page Docstring"""
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        # let today = new Date();
        # 'cert_date': ,
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game',
            'lbs': str(self.group.all_rounds_contribution()/10*22).split(" ")[0] + " lbs",
            'amount': c(self.group.all_rounds_contribution()).to_real_world_currency(self.session)
        }


class FinalResults(Page):
    """Page Docstring"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game',
            'goal_meet': Constants.group_goal <= self.group.all_rounds_contribution(),
            'carbonfund': self.group.all_rounds_contribution_in_dollars(),
            'quiz': c(self.player.how_many_good_answers()).to_real_world_currency(self.session)
        }

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def before_next_page(self):
        self.group.pay_carbonfund()
        self.group.pay_quizzes()



class PostSurvey1(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'survey_goals',
        'survey_goals_success',
        'survey_guiding_info',
        'survey_individual_conservation',
        'survey_group_conservation',
        'survey_rank_concentration',
        'survey_rank_understandable',
        'survey_rank_collective',
        'survey_rank_teamwork',
        'survey_rank_group',
        'survey_range_pastcontributions',
        'survey_range_totalgroup',
        'survey_range_totaloverall',
        'survey_range_percentgoal',
        'survey_range_envbenefit',
    ]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    """template variables"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game'
        }



class PostSurvey2(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'survey_help_others',
        'survey_share_ideas',
        'survey_learn_others',
        'survey_work_others',
        'survey_self_best',
        'survey_self_challenge',
        'survey_dislike_teamwork',
        'survey_bothered_teamwork',
        'survey_better_alone',
    ]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'progress': 'Survey',
            'aux': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        }


class PostSurvey3(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'survey_plants',
        'survey_marinelife',
        'survey_birds',
        'survey_animals',
        'survey_prosperity',
        'survey_lifestyle',
        'survey_health',
        'survey_future',
        'survey_community',
        'survey_children',
        'survey_unitedstates',
    ]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    """template variables"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Survey',
            'aux': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        }



class PostSurvey4(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        'survey_demographics_birthyear',
        'survey_demographics_gender',
        'survey_demographics_ethnicity',
        'survey_demographics_employment',
        'survey_demographics_experience',
        'survey_demographics_reliability',
        'survey_demographics_political',
        'survey_demographics_residency',
    ]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    """template variables"""
    def vars_for_template(self):
        return {
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Survey',
            'aux': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        }




class Debriefing(Page):
    """Page Docstring"""
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    """template variables"""
    def vars_for_template(self):
        return {'progress': 'End'}



page_sequence = [
    # IntroConsent,
    # IntroOutline,
    # IntroIntroduction,
    # IntroStructure,
    # IntroGameplay,
    # IntroFinancialOutcomes,
    # IntroEnvironOutcomes,
    # Examples,
    # Example1,
    # Example2,
    # Example3,
    # PracticeIntro,
    # PracticeGame,
    # PracticeResults,
    # Quiz,
    # Quiz1,
    # Quiz2,
    # IntroEnvironOutcomes,
    # Quiz2,
    # Quiz3,
    # Example2,
    # Example3,
    # Quiz3,
    # Quiz4,
    # Example1,
    # Quiz4,
    GameIntro,
    Game,
    ResultsWaitPage,
    Results,
    Congrats,
    FinalResults,
    PostSurvey1,
    PostSurvey2,
    PostSurvey3,
    PostSurvey4,
    Debriefing
]
