import random
from otree.api import Currency as c, currency_range
from .constants import Constants
from ._builtin import Page
from .utils import Utils


class Intro1(Page):
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
        return self.round_number == 1 \
            or self.round_number == 2 \
            and self.player.repeatQuiz1


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


class PracticeResults(Page):
    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        game_round = 1
        player_contribution = self.player.practice_contribution
        player_contribution_total = player_contribution
        player_withheld = c(10) - self.player.practice_contribution
        player_withheld_total = player_withheld
        group_contribution = c(147)
        group_contribution_total = group_contribution
        contributions_round = group_contribution + player_contribution
        contributions_total = contributions_round

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
        return self.player.qattempts("q1") <= 2 \
            and not self.player.qcorrect("q1")

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles[15],
            'progress': 'Quiz',
            'can_review': self.player.qattempts("q1") <= 0,
            'show_hint': self.player.qattempts("q1") > 0,
            'quiz_hint': Constants.quiz_default_hint,
            "answer_key": dict(q1=Constants.q1[0]["answer"])
        }

    def error_message(self, values):
        valid = self.player.valid_q1(values)
        if not valid:
            if self.player.qattempts("q1") <= 1:
                self.player.review_rules = 1


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']

    def is_displayed(self):
        return self.player.qattempts("q2") <= 2 \
            and not self.player.qcorrect("q2")

    def vars_for_template(self):
        return {
            'progress': 'Quiz',
            'participant.vars': self.player.participant.vars,
            'page_title': Constants.page_titles[16],
            'can_review': self.player.qattempts("q2") <= 0,
            'show_hint': self.player.qattempts("q2") > 0,
            'q2_attempts': self.player.qattempts("q2"),
            'q2_correct': self.player.qcorrect("q2"),
            'quiz_hint': Constants.quiz_default_hint,
            'answer_key': dict(q2=Constants.q2[0]["answer"]),
        }

    def error_message(self, values):
        valid = self.player.valid_q2(values)
        if not valid:
            if self.player.qattempts("q2") <= 1:
                self.player.review_rules = 2



class Quiz3(Page):
    form_model = 'player'
    form_fields = [
        'q3a',
        'q3b',
    ]

    def is_displayed(self):
        return (self.player.qattempts("q3a") <= 2) and not self.player.qcorrect("q3a") \
            or (self.player.qattempts("q3b") <= 2) and not self.player.qcorrect("q3b")


    def vars_for_template(self):
        return {
            'can_review': self.player.qattempts("q3a") <= 0,
            'page_title': Constants.page_titles[17],
            'participant_vars': self.player.participant.vars,
            'progress': 'Quiz',
            'show_hint': self.player.qattempts("q3a")  > 0 or self.player.qattempts("q3b") > 0,
            'answer_key': dict(
                q3a=Constants.q3[0]["answer"],
                q3b=Constants.q3[1]["answer"],
            ),
            'q3a_choices': Constants.q3[0]["choices"],
            'q3b_choices': Constants.q3[1]["choices"],
            'q3a_attempts': self.player.qattempts("q3a"),
            'q3b_attempts': self.player.qattempts("q3b"),
            'q3_hint': [
                Constants.q3[0]["hint"],
                Constants.q3[1]["hint"],
            ]
        }


    def error_message(self, values):
        valid = self.player.valid_q3(values)
        if not valid:
            if self.player.qattempts("q3a") <= 1:
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


    def is_displayed(self):
        iscorrect = [
            self.player.qcorrect("q4a"),
            self.player.qcorrect("q4b"),
            self.player.qcorrect("q4c"),
            self.player.qcorrect("q4d"),
            self.player.qcorrect("q4e"),
            self.player.qcorrect("q4f"),
        ]
        num_correct = 0
        for q in iscorrect:
            if q is True:
                num_correct += 1
        return self.player.qattempts("q4a") <= 2 \
            and not num_correct == 6



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
            'participant_vars': self.player.participant.vars,
            'can_review': self.player.qattempts("q4a"),
            'page_title': Constants.page_titles[18],
            'progress': 'Quiz',
            'show_hint': self.player.qattempts("q4a") > 0,
            'attempts': self.player.qattempts("q4a"),
            'answer_key': answer_key,
            'q4_hints': hint_text,
        }


    def error_message(self, values):
        valid = self.player.valid_q4(values)
        if valid is not True:
            print("valid", valid)
            if valid[0] is not True \
                or valid[1] is not True \
                or valid[2] is not True \
                or valid[3] is not True \
                or valid[4] is not True \
                or valid[5] is not True:
                if self.player.qattempts("q4a") <= 1:
                    self.player.review_rules = 4

    def before_next_page(self):
        self.player.finalize_data()



class ReviewGameRules(Page):

    def is_displayed(self):
        if self.player.review_rules == 1:
            return True
        elif self.player.review_rules == 2:
            return True
        elif self.player.review_rules == 3:
            return True
        elif self.player.review_rules == 4:
            return True
        else:
            return False

    def vars_for_template(self):
        page_title = 'Review Game Rules'
        table_classes = {}
        if self.player.review_rules == 1:
            page_title = 'Review: Game Structure'
        elif self.player.review_rules == 2:
            page_title = 'Review: Game Outcomes'
        elif self.player.review_rules == 3:
            page_title = 'Review: Examples Table'
            table_classes = {
                'row1': '',
                'row2': '',
                'row3': '',
                'row4': '',
                'row5': '',
            }
        elif self.player.review_rules == 4:
            page_title = 'Review: Example 1'
            table_classes = {
                'row1': 'outline-row',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': 'text-muted',
                'row5': 'text-muted',
            }

        return {
        'page_title': page_title,
            'reduction_goal': Constants.reduction_goal,
            'game_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
            'progress': 'Examples',
            'classes': table_classes
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
            'participant.vars': self.player.participant.vars,
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
    Quiz,
    Quiz1,
    ReviewGameRules,
    Quiz1,
    Quiz2,
    ReviewGameRules,
    Quiz2,
    Quiz3,
    ReviewGameRules,
    ReviewGameRules,
    Quiz3,
    Quiz4,
    ReviewGameRules,
    Quiz4,
    GameIntro,
]
