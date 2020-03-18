import random
import json
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .utils import Utils

def print_var(somevar, title=""):
    if title is not "":
        print(title)
    print(json.dumps(somevar, separators=(". ", ":"), indent=4))


class Intro1(Page):
    """Introduction: Consent Form"""
    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Consent',
            'page_title': Constants.page_titles[0]
        }


class Intro2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[1]
        }


class Intro3(Page):
    def is_displayed(self):
        return (self.round_number == 1 \
            or (self.round_number == 2) \
            and self.player.repeatQuiz1)


    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[2],
            'reduction_goal': Constants.reduction_goal,
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
        }



class Intro4(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        Utils.dump_obj(self)
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[3],
            'page_index': 2,
            'reduction_goal': Constants.reduction_goal,
            'optimal_contribution': '6',
            'game_tokens': Constants.game_tokens,
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'token_goal': Constants.game_goal,
            'token_value': Constants.token_value,
        }



class Intro5(Page):
    def is_displayed(self):
        return (self.round_number == 1)


    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[4],
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_value': Constants.token_value,
        }



class Intro6(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return  {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[5],
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_goal': Constants.token_goal,
            'token_value': Constants.token_value,
            'game_tokens': Constants.token_goal,
        }


class Intro7(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return  {
            'progress': 'Introduction',
            'page_title': Constants.page_titles[6],
            'game_players': '25',
            'optimal_contribution': '6',
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'game_tokens': Constants.game_tokens,
            'reduction_goal': Constants.reduction_goal,
            'token_value': Constants.token_value,
        }


class Examples(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[7],
            'progress': 'Examples'
        }


class Example1(Page):
    def is_displayed(self):
        return(self.round_number == 1)

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[8],
            'progress': 'Examples',
            'game_goal': '60',
            'classes': {
                'row1': '',
                'row2': 'hide',
                'row3': 'hide',
                'row4': 'hide',
                'row5': 'hide',
            },
        }


class Example2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[9],
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': '',
                'row3': '',
                'row4': 'hide',
                'row5': 'hide',
            }
        }


class Example3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[10],
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': '',
                'row5': '',
            }
        }



class PracticeIntro(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[11],
            'progress': 'Practice'
        }




class PracticeGame(Page):
    form_model = 'player'
    form_fields = [
        'practice_contribution'
    ]

    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[12],
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
        game_round = 1
        player_contribution = self.player.practice_contribution
        player_contribution_total = player_contribution
        player_withheld = 10 - self.player.practice_contribution
        player_withheld_total = player_withheld
        group_contribution = c(147)
        group_contribution_total = group_contribution
        contributions_round = group_contribution + player_contribution
        contributions_total = contributions_round
        group_contribution_total
        percent_goal = group_contribution_total * 100 / 900

        return {
            'progress': 'Practice',
            'page_title': Constants.page_titles[13],
            'current_month': Constants.MONTHS[game_round],
            'game_round': game_round,
            'current_round': game_round,
            'player_contribution': player_contribution,
            'player_contribution_total': player_contribution_total,
            'player_withheld': player_withheld,
            'player_withheld_total': player_withheld_total,
            'group_contribution': group_contribution,
            'group_contribution_total': group_contribution_total,
            'contributions_round': contributions_round,
            'contributions_total': contributions_total,
            'avg_contrib': contributions_total / Constants.game_players,
            'percent_goal': int(group_contribution_total * 100 / 900)
        }


class Quiz(Page):
    after_all_players_arrive = 'init_attempts'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[14],
            'progress': 'Quiz'
        }


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1']

    def is_displayed(self):
        return self.player.q1_attempts <= 2 and not self.player.q1_correct


    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[15],
            'progress': 'Quiz',
            'can_review': 0 >= self.player.q1_attempts,
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
            if self.player.q1_attempts <= 1:
                self.player.review_rules = 1


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'page_title': Constants.page_titles[16],
            'can_review': 0 >= self.player.q2_attempts,
            'show_hint': self.player.q2_attempts > Constants.quiz_max_attempts,
            'q2_attempts': self.player.q2_attempts,
            'q2_correct': self.player.q2_correct,
            'quiz_hint': Constants.quiz_default_hint,
            'answer_key': dict(q2=Constants.q2[0]["answer"]),
        }

    def is_displayed(self):
        return self.player.q2_attempts <= Constants.quiz_max_attempts \
            and not self.player.q2_correct

    def q2_choices(self):
        choices = Constants.q2[0]["choices"]
        random.shuffle(choices)
        return choices

    def error_message(self, values):
        valid = self.player.valid_q2(values)
        if not valid:
            if self.player.q2_attempts <= 1:
                self.player.review_rules = 2



class Quiz3(Page):
    form_model = 'player'
    form_fields = [
        'q3a',
        'q3b',
    ]

    def vars_for_template(self):
        return {
            'can_review': 0 >= self.player.q3a_attempts,
            'page_title': Constants.page_titles[17],
            'progress': 'Quiz',
            'show_hint': self.player.q3a_attempts > 1 or self.player.q3b_attempts > 1,
            'answer_key': dict(
                q3a=Constants.q3[0]["answer"],
                q3b=Constants.q3[1]["answer"],
            ),
            'q3a_choices': Constants.q3[0]["choices"],
            'q3b_choices': Constants.q3[1]["choices"],
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
        choices2 = Constants.q3[1]["choices"]
        random.shuffle(choices2)
        return choices2

    def error_message(self, values):
        valid = self.player.valid_q3(values)
        if not valid:
            if self.player.q3a_attempts <= 1:
                self.player.review_rules = 3



class Quiz4(Page):
    form_model = "player"
    form_fields = [
        "q4a",
        "q4b",
        "q4c",
        "q4d",
        "q4e",
        "q4f",
    ]

    def vars_for_template(self):
        answer_key = dict(
            q4a=Constants.q4[0]["answer"],
            q4b=Constants.q4[1]["answer"],
            q4c=Constants.q4[2]["answer"],
            q4d=Constants.q4[3]["answer"],
            q4e=Constants.q4[4]["answer"],
            q4f=Constants.q4[5]["answer"],
        )
        hint_text = [
            Constants.q4[0]["hint"],
            Constants.q4[1]["hint"],
            Constants.q4[2]["hint"],
            Constants.q4[3]["hint"],
            Constants.q4[4]["hint"],
            Constants.q4[5]["hint"],
        ]
        return {
            'can_review': 0 >= self.player.q4a_attempts,
            'page_title': Constants.page_titles[18],
            'progress': 'Quiz',
            'show_hint': self.player.q4a_attempts > 1,
            'attempts': self.player.q4a_attempts,
            'answer_key': answer_key,
            'q4_hints': hint_text,
        }


    def is_displayed(self):
        num_correct = 0
        iscorrect = [
            self.player.q4a_correct,
            self.player.q4b_correct,
            self.player.q4c_correct,
            self.player.q4d_correct,
            self.player.q4e_correct,
            self.player.q4f_correct,
        ]
        for q in iscorrect:
            if q is True:
                num_correct += 1

        if self.player.q4a_attempts < Constants.quiz_max_attempts \
            and num_correct == 6:
            return False
        else:
            return True


    def error_message(self, values):
        valid = self.player.valid_q4(values)
        print(valid)
        if valid[0] is not True \
            or valid[1] is not True \
            or valid[2] is not True \
            or valid[3] is not True \
            or valid[4] is not True \
            or valid[5] is not True:
            if self.player.q4a_correct <= 1:
                self.player.review_rules = 4




class ReviewGameRules(Page):
    template_name = 'onboarding_app/Example3.html'

    def is_displayed(self):
        print('Should we review the rule', self.player.review_rules)
        if self.player.review_rules <= 0:
            return False
        elif self.player.review_rules == 1:
            template_name = 'onboarding_app/Intro3.html'
            page_title = 'Review: Game Structure'
            return True
        elif self.player.review_rules == 2:
            template_name = 'onboarding_app/Intro7.html'
            page_title = 'Review: Game Outcomes'
            return True
        elif self.player.review_rules == 3:
            template_name = 'onboarding_app/ExampleAll.html'
            page_title = 'Review: Examples'
            return True
        elif self.player.review_rules == 4:
            template_name = 'onboarding_app/Example1.html'
            page_title = 'Review: Example 1'
            return True
        else:
            return False

    def vars_for_template(self):
        return {
            'page_title': 'Review Game Rules',
            'progress': 'Examples',
            'classes': {
                'row1': 'outline-row',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': 'text-muted',
                'row5': 'text-muted',
            }
        }

    def before_next_page(self):
        self.player.review_rules = 0


class GameIntro(Page):
    def is_displayed(self):
        return self.round_number >= 1

    def before_next_page(self):
        self.player.finalize_data()

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[19],
            'progress': 'Game'
        }


page_sequence = [
    Intro1,
    Intro2,
    Intro3,
    Intro4,
    Intro5,
    Intro6,
    Intro7,
    Examples,
    Example1,
    Example2,
    Example3,
    PracticeIntro,
    PracticeGame,
    PracticeResults,
    Quiz,            # QUIZ
    Quiz1,           # Q1
    ReviewGameRules, # -- REVIEW
    Quiz1,           # Q1
    Quiz2,           # Q2
    ReviewGameRules, # -- REVIEW
    Quiz2,
    Quiz3,           # Q3
    ReviewGameRules, # Example2,
    ReviewGameRules, # Example3,
    Quiz3,
    Quiz4,           # Q4
    ReviewGameRules, # Example1,
    Quiz4,
    GameIntro,
]
