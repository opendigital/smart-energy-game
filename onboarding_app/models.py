import json
import inspect
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Matt Harris'

doc = """
RCODI Energy Game Pre-game training
"""

class Constants(BaseConstants):

    template_config = dict(
        debug_vars=False,
        debug_jsvars=False
    )

    name_in_url = 'onboarding'
    players_per_group = None
    num_rounds = 1
    reduction_goal = 60
    game_rounds = 6
    game_tokens = 10
    game_players = 25
    game_goal = 900
    token_goal = 6
    token_value = .01
    quiz_max_attempts = 2

    page_titles = [
        "Research Participant Consent Form",
        "Instruction: Game Outline",
        "Instruction: Game Structure and Incentives",
        "Instruction: Introduction",
        "Instruction: Gameplay",
        "Instruction: Financial Outcomes",
        "Instruction: Environmental Outcomes",
        "Examples: Overview",
        "Examples: 1. Minimum Requirement",
        "Examples: 2 and 3. Min and Max Conservation",
        "Examples: 4 and 5. Only You and Everyone But You",
        "Practice: Game Intro",
        "Practice: Game",
        "Practice: Game Result",
        "Comprehension: Quiz",
        "Comprehension: Quiz 1/4",
        "Comprehension: Quiz 2/4",
        "Comprehension: Quiz 3/4",
        "Comprehension: Quiz 4/4",
        "Game: Introduction",
    ]


    true_false = [
        "True",
        "False"
    ]

    MONTHS = [
        'JANUARY',
        'FEBRUARY',
        'MARCH',
        'APRIL',
        'MAY',
        'JUNE',
        'JULY',
        'AUGUST',
        'SEPTEMBER',
        'OCTOBER',
        'NOVEMBER',
        'DECEMBER'
    ]

    quiz_default_hint = 'Please proceed to Review Instructions. \
        You will then return to this question and have one \
        more opportunity to answer it'


    q1 = [
        dict(
            label="On average, how many tokens will each player need to invest into the group conservation account in each round in order to meet the 60% group conservation goal",
            choices=["2 tokens", "3 tokens", "6 tokens", "11 tokens"],
            answer="6 tokens",
            hint="To meet the 60% energy conservation goal, each player should contribute 6 energy \
                tokens each month to the group conservation account, resulting in 900 energy \
                tokens at the end of the game.",
        )
    ]

    q2 = [
        dict(
            label='For each energy token in the group conservation account $0.01 is contributed to Carbonfund.org to reduce actual air pollution in the real world',
            choices=true_false,
            answer='True',
            hint='Each token in the group conservation account equals $0.01 dollars. The \
                dollar value of the group conservation account is contributed to Carbonfund.org.',
        )
    ]

    q3 = [
        dict(
            label="You will have greater earnings than others if you put all of your energy tokens in your private account, while others contribute all of theirs to the group conservation account",
            choices=true_false,
            answer="True",
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label='True or False: The group will maximize its earning if all players contribute 6 of their energy tokens to the group conservation account each month',
            choices=true_false,
            answer="True",
            hint="The group gets the maximum financial payment if all players contribute \
                all 10 tokens in the conservation account in each month (25 players \
                &times; 10 tokens &times; 6 months &times; $.01 = $15). Every player then gets an equal \
                share of the maximum bonus possible, which is double the value of the \
                tokens in the conservation account (2 &times; $15 &divide; 25 players = $1.20).",
        )
    ]

    q4 = [
        dict(
            label="My payout from my private account is",
            answer=2,
            choices=[
                [1, "$0.00"],
                [2, "$0.30"],
                [3, "$3.00"],
            ],
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label="My bonus payout from the group conservation account is",
            answer=1,
            choices=[
                [1, "$0.72"],
                [2, "$1.00"],
                [3, "$2.72"],
            ],
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 &divide; 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        ),
        dict(
            label="Total payout is (private plus group conservation bonus)",
            answer=2,
            choices=[
                [1, "$0.50"],
                [2, "$1.02"],
                [3, "$3.72"],
            ],
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label="My payout from my personal account is",
            answer=2,
            choices=[
                [1, "$0.00"],
                [2, "$0.30"],
                [3, "$3.00"],
            ],
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 &divide; 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        ),
        dict(
            label="My payout from the group conservation account is",
            answer=1,
            choices=[
                [1, "$0.00"],
                [2, "$1.00"],
                [3, "$2.00"],
            ],
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label="Total payout is (private plus group conservation bonus)",
            answer=2,
            choices=[
                [1, "$0.00"],
                [2, "$0.30"],
                [3, "$3.00"]
            ],
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 &divide; 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        )
    ]



# _ Session
# num_participants
# config
# vars

class Subsession(BaseSubsession):
    # BUILTIN:
    # __ session
    # __ round_number
    # __ creating_session()
    # __ get_groups()
    # __ get_players()
    # __ group_randomly()
    # __ group_like_round()
    # __ get_group_matrix()
    # __ set_group_matrix()
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)

    def get_quiz_group(self, index):
        return [
            Constants.q1,
            Constants.q2,
            Constants.q3,
            Constants.q4
        ][index]

    def get_keys_from_quiz_group(self, index):
        answers = []
        group = self.get_quiz_group(index)
        for field in group:
            answers.append(field["answer"])
        return answers

    def get_all_keys_from_quiz_group(self):
        return [
            self.get_keys_from_quiz_group(0),
            self.get_keys_from_quiz_group(1),
            self.get_keys_from_quiz_group(2),
            self.get_keys_from_quiz_group(3),
        ]

    def creating_session(self):
        print('in creating_session', self.round_number)
        self.session.vars["quizdata"] = 'test'
        session_answers = self.get_all_keys_from_quiz_group()
        self.session.vars["answer_key"] = session_answers

    def review_rulepage(self):
        print('review_rulepage')
        return []

    def init_attempts(self):
        return dict(
            q1=0,
            q2=0,
            q3a=0,
            q3b=0,
            q4a=0,
            q4b=0,
            q4c=0,
            q4d=0,
            q4e=0,
            q4f=0,
        )



class Group(BaseGroup):
    # BUILTIN:
    # __ session/subsession
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)
    # __ get_player_by_role(role)
    # __ get_player_by_id(id_in_group)
    # __ get_players()
    pass


# _ Participant
# id_in_session
# vars
# label
# payoff
# payoff_plus_participation_fee
#
class Player(BasePlayer):
    # BUILTIN:
    # __ payoff
    # __ session/subsession/group/participant
    # __ id_in_group
    # __ role()
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)
    # __ get_others_in_subsession()
    # __ get_others_in_group()
    #

    participant_vars_dump = models.LongStringField()
    quiz_result = models.LongStringField()
    page_attempts = models.IntegerField(initial=0)
    review_rules = models.IntegerField(initial=0)
    practice_contribution = models.CurrencyField(min=0, max=10)
    practice_private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()


    def finalize_data(self):
        self.participant.vars['quiz_result'] = str([
            self.q1_attempts,
            self.q2_attempts,
            self.q3a_attempts,
            self.q3b_attempts,
            self.q4a_attempts,
            self.q4b_attempts,
            self.q4c_attempts,
            self.q4d_attempts,
            self.q4e_attempts,
            self.q4f_attempts,
        ])
        self.participant.vars['quiz_bonus'] = self.payoff
        print(self.participant.vars)

    def quiz_bonus(self):
        self.payoff += 5

    def init_quiz_count(self):
        self.participant.vars['object has no attribute blah'] = [1, 2, 3]

    def dump_participant_vars(self):
        self.player.participant_vars_dump = str(self.participant.vars)

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_contribution(self):
        return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_private_contribution(self):
        return sum([p.practice_private_contribution for p in self.in_rounds(1, self.round_number)])


    def validate_field(self, id, value, answer):
        print('validating field', id)


    def valid_q1(self, values):
        if self.q1_correct == True:
            return True

        self.q1_attempts += 1
        quiz_index = 0
        answers = self.session.vars["answer_key"][quiz_index]

        if self.q1 == answers[0] or values["q1"] == answers[0]:
            self.q1_correct = True
            if self.q1_attempts <= 1:
                self.quiz_bonus()
            return True
        else:
            return False


    def valid_q2(self, values):
        if self.q2_correct == True:
            return True

        self.q2_attempts += 1
        quiz_index = 1
        answers = self.session.vars["answer_key"][quiz_index]

        if self.q2 == answers[0] or values["q2"] == answers[0]:
            self.q2_correct = True
            if self.q2_attempts <= 1:
                self.quiz_bonus()
            return True
        else:
            return False


    def valid_q3(self, values):
        if self.q3a_correct and self.q3b_correct:
            return True

        quiz_index = 2
        answers = self.session.vars["answer_key"][quiz_index]

        if self.q3a_correct is not True:
            self.q3a_attempts += 1
            if self.q3a == answers[0] or values["q3a"] == answers[0]:
                self.q3a_correct = True
                if self.q3a_attempts <= 1:
                    self.quiz_bonus()

        if self.q3b_correct is not True:
            self.q3b_attempts += 1
            if self.q3b == answers[1] or values["q3b"] == answers[1]:
                self.q3b_correct = True
                if self.q3b_attempts <= 1:
                    self.quiz_bonus()

        if self.q3a_correct and self.q3b_correct:
            return True
        return False




    def valid_q4(self, values):
        quiz_index = 3
        answers = self.session.vars["answer_key"][quiz_index]

        if self.q4a_correct is not True:
            self.q4a_attempts += 1
            if self.q4a == answers[0] or values["q4a"] == answers[0]:
                self.q4a_correct = True
                if self.q4a_attempts <= 1:
                    self.quiz_bonus()

        if self.q4b_correct is not True:
            self.q4b_attempts += 1
            if self.q4b == answers[1] or values["q4b"] == answers[1]:
                self.q4b_correct = True
                if self.q4b_attempts <= 1:
                    self.quiz_bonus()

        if self.q4c_correct is not True:
            self.q4c_attempts += 1
            if self.q4c == answers[2] or values["q4c"] == answers[2]:
                self.q4c_correct = True
                if self.q4c_attempts <= 1:
                    self.quiz_bonus()

        if self.q4d_correct is not True:
            self.q4d_attempts += 1
            if self.q4d == answers[3] or values["q4d"] == answers[3]:
                self.q4d_correct = True
                if self.q4d_attempts <= 1:
                    self.quiz_bonus()

        if self.q4e_correct is not True:
            self.q4e_attempts += 1
            if self.q4e == answers[4] or values["q4e"] == answers[4]:
                self.q4e_correct = True
                if self.q4e_attempts <= 1:
                    self.quiz_bonus()

        if self.q4f_correct is not True:
            self.q4f_attempts += 1
            if self.q4f == answers[5] or values["q4f"] == answers[5]:
                self.q4f_correct = True
                if self.q4f_attempts <= 1:
                    self.quiz_bonus()

        q4_all_correct = [
            self.q4a_correct,
            self.q4b_correct,
            self.q4c_correct,
            self.q4d_correct,
            self.q4e_correct,
            self.q4f_correct,
        ]

        return q4_all_correct


    # QUIZES
    # ===========================================
    q1 = models.StringField(
        label=Constants.q1[0]["label"],
        widget=widgets.RadioSelect,
    )
    q1_attempts = models.IntegerField(initial=0)
    q1_correct = models.BooleanField(initial=False)

    q2 = models.StringField(
        label=Constants.q2[0]["label"],
        widget=widgets.RadioSelect
    )
    q2_attempts = models.IntegerField(initial=0)
    q2_correct = models.BooleanField(initial=False)

    q3a = models.StringField(
        label=Constants.q3[0]["label"],
        widget=widgets.RadioSelect
    )
    q3a_correct = models.BooleanField(initial=False)
    q3a_attempts = models.IntegerField(initial=0)

    q3b = models.StringField(
        label=Constants.q3[1]["label"],
        widget=widgets.RadioSelect
    )
    q3b_correct = models.BooleanField(initial=False)
    q3b_attempts = models.IntegerField(initial=0)

    q4a = models.IntegerField(
        label=Constants.q4[0]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[0]["choices"]
    )

    q4b = models.IntegerField(
        label=Constants.q4[1]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[1]["choices"]
    )

    q4c = models.IntegerField(
        label=Constants.q4[2]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[2]["choices"]
    )

    q4d = models.IntegerField(
        label=Constants.q4[3]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[3]["choices"]
    )

    q4e = models.IntegerField(
        label=Constants.q4[4]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[4]["choices"]
    )

    q4f = models.IntegerField(
        label=Constants.q4[5]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[5]["choices"]
    )

    q4a_attempts = models.IntegerField(initial=0)
    q4a_correct = models.BooleanField(initial=False)
    q4b_attempts = models.IntegerField(initial=0)
    q4b_correct = models.BooleanField(initial=False)
    q4c_attempts = models.IntegerField(initial=0)
    q4c_correct = models.BooleanField(initial=False)
    q4d_attempts = models.IntegerField(initial=0)
    q4d_correct = models.BooleanField(initial=False)
    q4e_attempts = models.IntegerField(initial=0)
    q4e_correct = models.BooleanField(initial=False)
    q4f_attempts = models.IntegerField(initial=0)
    q4f_correct = models.BooleanField(initial=False)
