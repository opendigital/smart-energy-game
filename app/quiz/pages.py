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
            'page_title': Constants.page_titles["intro1"]
        }



class Intro2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles["intro2"]
        }



class Intro3(Page):
    def is_displayed(self):
        return self.round_number == 1 \
            or self.round_number == 2 \
            and self.player.repeatQuiz1


    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles["intro3"],
            'reduction_goal': Constants.reduction_goal,
            'game_players': Constants.game_players,
            'other_players': Constants.game_players - 1,
            'game_rounds': Constants.game_rounds,
        }



class Intro4(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'progress': 'Introduction',
            'page_title': Constants.page_titles["intro4"],
            'page_index': 2,
            'reduction_goal': Constants.reduction_goal,
            'optimal_contribution': '6',
            'game_tokens': Constants.game_tokens,
            'game_players': Constants.game_players,
            'other_players': Constants.game_players - 1,
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
            'page_title': Constants.page_titles["intro5"],
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
            'page_title': Constants.page_titles["intro6"],
            'optimal_contribution': '6',
            'game_players': Constants.game_players,
            'other_players': Constants.game_players - 1,
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
            'page_title': Constants.page_titles["intro7"],
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
            'page_title': Constants.page_titles["examples"],
            'progress': 'Examples'
        }



class Example1(Page):
    def is_displayed(self):
        return(self.round_number == 1)

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["example1"],
            'progress': 'Examples',
            'game_goal': '60',
            'classes': {
                'row1': 'bg-grey300',
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
            'page_title': Constants.page_titles["example2"],
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'bg-grey300',
                'row3': 'bg-grey300',
                'row4': 'hide',
                'row5': 'hide',
            }
        }



class Example3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["example3"],
            'progress': 'Examples',
            'classes': {
                'row1': 'text-muted',
                'row2': 'text-muted',
                'row3': 'text-muted',
                'row4': 'bg-grey300',
                'row5': 'bg-grey300',
            }
        }



class PracticeIntro(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["practiceintro"],
            'progress': 'Practice'
        }



class PracticeGame1(Page):
    template_name = './quiz/PracticeGame.html'
    form_model = 'player'
    form_fields = [
        'practice_contrib1'
    ]

    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'page_title': Constants.page_titles["practicegame1"],
            'progress': 'Practice',
            'field_name': 'practice_contrib1',
            'current_month': round_month,
            'current_round': 0,
        }



class PracticeGame2(Page):
    template_name = './quiz/PracticeGame.html'
    form_model = 'player'
    form_fields = [
        'practice_contrib2'
    ]

    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index + 1)
        return {
            'page_title': Constants.page_titles["practicegame2"],
            'progress': 'Practice',
            'field_name': 'practice_contrib2',
            'current_month': round_month,
            'current_round': 0,
        }



class PracticeResults1(Page):
    template_name = './quiz/PracticeResults.html'
    def is_displayed(self):
        return self.round_number <= 1

    def vars_for_template(self):
        game_round = self.round_number
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        player_contribution = self.player.practice_contrib1
        player_contribution_total = player_contribution
        player_withheld = c(10) - self.player.practice_contrib1
        player_withheld_total = player_withheld
        group_contribution = c(147)
        group_contribution_total = group_contribution
        contributions_round = group_contribution + player_contribution
        contributions_total = contributions_round
        percent_goal = int(group_contribution_total * 100 / 900)
        return {
            'progress': 'Practice',
            'page_title': Constants.page_titles["practiceresults1"],
            'current_month': round_month,
            'game_round': 1,
            'current_round': 0,
            'player_contribution': player_contribution,
            'player_contribution_total': player_contribution_total,
            'player_withheld': player_withheld,
            'player_withheld_total': player_withheld_total,
            'group_contribution': group_contribution,
            'group_contribution_total': group_contribution_total,
            'contributions_round': contributions_round,
            'contributions_total': contributions_total,
            'avg_contrib': contributions_total / Constants.game_players,
            'percent_goal': percent_goal
        }



class PracticeResults2(Page):
    template_name = './quiz/PracticeResults.html'
    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        game_round = self.round_number
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        player_contribution = self.player.practice_contrib2
        player_contribution_total = self.player.practice_contrib1 + self.player.practice_contrib2
        player_withheld = c(10) - self.player.practice_contrib2
        player_withheld_total = c(20) - player_contribution_total
        group_contribution = c(143)
        group_contribution_total = c(147) + group_contribution
        contributions_round = group_contribution + player_contribution
        contributions_total = c(143) + c(147) + player_contribution_total
        percent_goal = int(group_contribution_total * 100 / 900)
        return {
            'progress': 'Practice',
            'page_title': Constants.page_titles["practiceresults2"],
            'current_month': round_month,
            'game_round': 2,
            'current_round': 0,
            'player_contribution': player_contribution,
            'player_contribution_total': player_contribution_total,
            'player_withheld': player_withheld,
            'player_withheld_total': player_withheld_total,
            'group_contribution': group_contribution,
            'group_contribution_total': group_contribution_total,
            'contributions_round': contributions_round,
            'contributions_total': contributions_total,
            'avg_contrib': contributions_total / 2 / Constants.game_players,
            'percent_goal': percent_goal
        }


class Summary(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return  {
            'progress': 'Practice',
            'page_title': 'Summary',
        }


class Quiz(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["quiz"],
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
            'page_title': Constants.page_titles["quiz1"],
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
            'page_title': Constants.page_titles["quiz2"],
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
    ]

    def is_displayed(self):
        return (self.player.qattempts("q3a") <= 2) and not self.player.qcorrect("q3a")

    def vars_for_template(self):
        return {
            'can_review': self.player.qattempts("q3a") <= 0,
            'page_title': Constants.page_titles["quiz3"],
            'participant_vars': self.player.participant.vars,
            'progress': 'Quiz',
            'show_hint': self.player.qattempts("q3a")  > 0 or self.player.qattempts("q3b") > 0,
            'answer_key': dict(
                q3a=Constants.q3[0]["answer"],
                q3b=Constants.q3[1]["answer"],
            ),
            'q3a_choices': Constants.q3[0]["choices"],
            'q3_hint': [
                Constants.q3[0]["hint"],
            ]
        }

    def error_message(self, values):
        valid = self.player.valid_q3(values)
        if not valid:
            print("q3 valid", valid)
            if self.player.qattempts("q3a") <= 1:
                self.player.review_rules = 3
                print("review ", self.player.review_rules)


class Quiz3b(Page):
    form_model = 'player'
    form_fields = [
        'q3b',
    ]

    def is_displayed(self):
        return (self.player.qattempts("q3b") <= 2) and not self.player.qcorrect("q3b")

    def vars_for_template(self):
        return {
            'can_review': self.player.qattempts("q3b") <= 0,
            'page_title': Constants.page_titles["quiz3b"],
            'participant_vars': self.player.participant.vars,
            'progress': 'Quiz',
            'show_hint': self.player.qattempts("q3b")  > 0,
            'answer_key': dict(
                q3b=Constants.q3[1]["answer"],
            ),
            'q3b_choices': Constants.q3[1]["choices"],
            'q3b_hint': Constants.q3[1]["hint"],
        }

    def error_message(self, values):
        valid = self.player.valid_q3b(values)
        if not valid:
            print("q3 valid", valid)
            if self.player.qattempts("q3b") <= 1:
                self.player.review_rules = 3
                print("review ", self.player.review_rules)



class Quiz4(Page):
    form_model = "player"
    form_fields = [
        "q4a",
        "q4b",
        "q4c",
    ]

    def is_displayed(self):
        if self.player.qcorrect("q4a") \
            and self.player.qcorrect("q4b") \
            and self.player.qcorrect("q4c"):
            return False
        else:
            if self.player.q4_total_attempts() <= 3:
                return True
            return False

    def vars_for_template(self):
        answer_key = dict(
            q4a=Constants.q4[0]["answer"],
            q4b=Constants.q4[1]["answer"],
            q4c=Constants.q4[2]["answer"],
        )

        hint_text = [
            Constants.q4[0]["hint"],
            Constants.q4[1]["hint"],
            Constants.q4[2]["hint"],
        ]

        return {
            'page_title': Constants.page_titles["quiz4"],
            'progress': 'Quiz',
            'participant_vars': self.player.participant.vars,
            'can_review': self.player.qattempts("q4a"),
            'show_hint': self.player.qattempts("q4a") > 0,
            'attempts': self.player.qattempts("q4a"),
            'answer_key': answer_key,
            'q4_hints': hint_text,
        }

    def error_message(self, values):
        valid = self.player.valid_q4(values)
        print('valid', valid)
        if valid is not True:
            if self.player.q4_total_attempts() <= 3:
                self.player.review_rules = 4


class Quiz4b(Page):
    form_model = "player"
    form_fields = [
        "q4d",
        "q4e",
        "q4f",
    ]

    def is_displayed(self):
        if self.player.qcorrect("q4d") \
            and self.player.qcorrect("q4e") \
            and self.player.qcorrect("q4f"):
            return False
        else:
            if self.player.q4b_total_attempts() <= 3:
                return True
            return False

    def vars_for_template(self):
        answer_key = dict(
            q4d=Constants.q4[3]["answer"],
            q4e=Constants.q4[4]["answer"],
            q4f=Constants.q4[5]["answer"],
        )

        hint_text = [
            Constants.q4[3]["hint"],
            Constants.q4[4]["hint"],
            Constants.q4[5]["hint"],
        ]

        return {
            'page_title': Constants.page_titles["quiz4b"],
            'progress': 'Quiz',
            'participant_vars': self.player.participant.vars,
            'can_review': self.player.qattempts("q4d"),
            'show_hint': self.player.qattempts("q4d") > 0,
            'attempts': self.player.qattempts("q4d"),
            'answer_key': answer_key,
            'q4_hints': hint_text,
        }

    def error_message(self, values):
        valid = self.player.valid_q4b(values)
        if valid is not True:
            if self.player.q4b_total_attempts() <= 3:
                self.player.review_rules = 5


# FAKE WAITING ROOM
# NOTE: CANNOT USE THE WORD 'FAKE'
# AS IT SHOWS IN THE UP URL
class WaitRoom(Page):
    template_name = './quiz/waiting-room.html'
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    after_all_players_arrive = 'finalize_group_round_data'

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
        'progress': 'Game',
        'page_title': 'Energy Conservation Game',
        'current_month': round_month,
        'current_round': self.round_number,
        }


class ReviewGameRules(Page):
    def is_displayed(self):
        if self.player.review_rules == 1 \
            or self.player.review_rules == 2 \
            or self.player.review_rules == 3 \
            or self.player.review_rules == 4 \
            or self.player.review_rules == 5:
            return True
        else:
            return False

    def vars_for_template(self):
        page_title = Constants.page_titles["reviewgamerules"]
        table_classes = {}
        if self.player.review_rules == 1:
            page_title = 'Review: Game Structure and Incentives'
        elif self.player.review_rules == 2:
            page_title = 'Review: Environmental Outcomes'
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
        elif self.player.review_rules == 5:
            page_title = 'Review: Financial Outcomes'

        return {
            'optimal_contribution': '6',
            'page_title': page_title,
            'game_players': Constants.game_players,
            'other_players': Constants.game_players - 1,
            'game_tokens': Constants.game_tokens,
            'token_value': Constants.token_value,
            'reduction_goal': Constants.reduction_goal,
            'game_rounds': Constants.game_rounds,
            'progress': 'Examples',
            'classes': table_classes,
            'token_goal': Constants.token_goal,
        }

    def before_next_page(self):
        self.player.review_rules = 0



class GameIntro(Page):
    def is_displayed(self):
        return self.round_number >= 1


    def vars_for_template(self):
        return {
            'participantvars': self.player.participant.vars,
            'page_title': Constants.page_titles["gameintro"],
            'progress': 'Game'
        }

    def before_next_page(self):
        self.player.finalize_data()



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
    PracticeGame1,
    PracticeResults1,
    PracticeGame2,
    PracticeResults2,
    Summary,
    Quiz,
    Quiz1,
    ReviewGameRules,
    Quiz1,
    Quiz2,
    ReviewGameRules,
    Quiz2,
    Quiz3,
    ReviewGameRules,
    Quiz3,
    Quiz3b,
    ReviewGameRules,
    Quiz3b,
    Quiz4,
    ReviewGameRules,
    Quiz4,
    Quiz4b,
    ReviewGameRules,
    Quiz4b,
    WaitRoom,
    GameIntro,
]
