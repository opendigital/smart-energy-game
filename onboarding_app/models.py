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


author = 'Your name here'

doc = """
Your app description
"""


def isset(arg):
    print("testing argument", arg)
    try:
        arg
    except NameError:
        arg = None
        print("except NameError", arg)

    if arg is None:
        print("arg is None", arg)
        return False
    else:
        print("returning argument", arg)
        return True


class Constants(BaseConstants):
    name_in_url = 'onboarding_app'
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
            label="On average, how many tokens will each player need \
                to invest into the group conservation account in each round in order \
                to meet the 60% group conservation goal?",
            choices=["2 tokens", "3 tokens", "6 tokens", "11 tokens"],
            answer="6 tokens",
            hint="To meet the 60% energy conservation goal, each player should contribute 6 energy \
                tokens each month to the group conservation account, resulting in 900 energy \
                tokens at the end of the game.",
        )
    ]

    q2 = [
        dict(
            label='For each energy token in the group conservation \
                account $0.01 is contributed to Carbonfund.org to reduce actual \
                air pollution in the real world?',
            choices=true_false,
            answer='True',
            hint='Each token in the group conservation account equals $0.01 dollars. The \
                dollar value of the group conservation account is contributed to Carbonfund.org.',
        )
    ]

    q3 = [
        dict(
            label="You will have greater earnings than others if you put all of your \
                energy tokens in your private account, while others contribute all of theirs to the \
                group conservation account.",
            choices=true_false,
            answer="True",
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label='True or False: The group will maximize its earning if all players contribute 6 of \
                their energy tokens to the group conservation account each month.',
            choices=true_false,
            answer="True",
            hint="The group gets the maximum financial payment if all players contribute \
                all 10 tokens in the conservation account in each month (25 players \
                &times; 10 tokens &times; 6 months &times; $.01 = $15). Every player then gets an equal \
                share of the maximum bonus possible, which is double the value of the \
                tokens in the conservation account (2 &times; $15 / 25 players = $1.20).",
        )
    ]

    q4 = [
        dict(
            label="My payout from my personal account is",
            answer="$1.00",
            choices=["$0.00", "$1.00", "$2.00"],
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label='Total payou"$1.t is (personal plus conservation)',
            choices=["$6.00", "$8.00", "$16.00"],
            answer="$18.18",
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 / 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        ),
        dict(
            label="My payout from my personal account is",
            choices=[
                "$7.00",
                "$10.00",
                "$17.00"
            ],
            answer="$19.18",
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label='My payout from my personal account is',
            choices=["$0.00", "$1.00", "$2.00"],
            answer="$1.00",
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 / 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        ),
        dict(
            label="My payout from the group conservation account is",
            choices=["$0.00", "$0.80", "$2.00"],
            answer="$0.00",
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table",
        ),
        dict(
            label='Total payout is (personal plus conservation)',
            choices=["$1.00", "$1.80", "$3.00"],
            answer="$1.00",
            hint="The group gets the maximum financial payment if all players contribute all 10 tokens in the \
                conservation account in each month (25 players &times; 10 tokens &times; 6 months &times; $.01 = $15). \
                Every player then gets an equal share of the maximum bonus possible, which is \
                double the value of the tokens in the conservation account (2 &times; $15 / 25 players = $1.20). \
                (If wrong take back to 2nd page of EXAMPLES: half a table)",
        )
    ]



class Subsession(BaseSubsession):
    def creating_session(self):
        print('in creating_session', self.round_number)
        self.session.vars["quizdata"] = 'test'
        for p in self.get_players():
            p.payoff = c(10)

    def review_rulepage(self):
        print('review_rulepage')
        return []

    def init_attempts(self):
        print('init_attempts')
        return dict(
            q1=0,
            q2=0,
            q3a=0,
            q3b=0,
            q4a1=0,
            q4a2=0,
            q4a3=0,
            q4b1=0,
            q4b2=0,
            q4b3=0,
        )



class Group(BaseGroup):
    pass


class Player(BasePlayer):

    page_attempts = models.IntegerField(initial=0)
    review_rules = models.IntegerField(initial=0)


    def dump(obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))

    def init_quiz_count(self):
        self.participant.vars['blah'] = [1, 2, 3]

    def var_exists(self, arg):
        print("test player.vars", arg, self.player.vars)
        if arg in self.player.vars:
            return self.player[arg]

    def dump_participant_vars(self):
        self.player.participant_vars_dump = str(self.participant.vars)


    def validate_field(self, id, value, answer):
        print('validating field', id)
        print(self.id)
        # if value == True:


    def validate_page(self, value_set, key_set):
        print('validating field', id)
        print(self.id)



    def valid_q1(self, values):
        print('CHECKING Q1 QUESTIONS', values)
        print('q1_current', self.q1)
        print('q1_correct', self.q1_correct)
        print('q1_attempts', self.q1_attempts)
        print('q1_answer', Constants.q1[0]["answer"])
        if self.q1_correct == True:
            print('already correct returning')
            return True

        if isset(self.q1) is not True:
            return False

        if self.q1 == Constants.q1[0]["answer"]:
            print('q1 is the correct answer')
            self.q1_attempts += 1
            self.q1_correct = True

            if self.q1_attempts <= 1:
                print('got it on the fist attempt for bonus')
                self.payoff += 5

            print('returning q1_is_valid')
            return True

        else:
            print('not returning q1_is_valid')
            return False

        return self.q1_correct


    def valid_q2(self, values):
        print('CHECKING Q2 QUESTIONS', values)
        print('q2_current', self.q2)
        print('q2_correct', self.q2_correct)
        print('q2_attempts', self.q2_attempts)
        print('q2_answer', Constants.q2[0]["answer"])
        if self.q2_correct == True:
            print('already correct returning')
            return True

        if isset(self.q2) is not True:
            return False

        if self.q2 == Constants.q2[0]["answer"]:
            print('q2 is the correct answer')
            self.q2_attempts += 1
            self.q2_correct = True
            if self.q2_attempts <= 1:
                print('got it on the fist attempt for bonus')
                self.payoff += 5

            print('returning q1_is_valid')
            return True

        print("quiz 2 attempts", self.q2_attempts)
        self.q2_attempts += 1

        if self.q2 == Constants.q2[0]["answer"]:
            self.q2_correct = True

            if self.q2_attempts == 1:
                print("first try", self.q2_attempts)
                self.payoff += 5

        return self.q2 == Constants.q2[0]["answer"]


    def valid_q3(self, values):
        print('CHECKING Q3 QUESTIONS', values)
        print('q3_current', self.q3a, self.q3b)
        print('q3a_correct', self.q3a_correct, self.q3b_correct)
        print('q3a_attempts', self.q3a_attempts)
        print('q3b_attempts', self.q3b_attempts)
        print('q3_answer', Constants.q3[0]["answer"])
        print('q3_answer', Constants.q3[1]["answer"])

        if self.q3a_correct == True and self.q3b_correct == True:
            print('already correct returning')
            return True

        if isset(self.q3a) is not True or isset(self.q3b) is not True:
            return False

        if self.q3a == Constants.q3[0]["answer"]:
            print('q3a is the correct answer')
            self.q3a_attempts += 1
            self.q3a_correct = True

        if self.q3b == Constants.q3[0]["answer"]:
            print('q3a is the correct answer')
            self.q3a_attempts += 1
            self.q3a_correct = True


            if self.q3a_attempts <= 1:
                print('got it on the fist attempt for bonus')
                self.payoff += 5

            print('returning q1_is_valid')
            return True

        self.q3a_attempts += 1
        print("quiz 2 attempts", self.q3a_attempts)
        #         if self.q3_attempts == 1:
        #             self.payoff += 5
        return self.q3 == Constants.q3[0]["answer"]


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

    q3b = models.BooleanField(
        label=Constants.q3[1]["label"],
        widget=widgets.RadioSelect
    )
    q3b_correct = models.BooleanField(initial=False)
    q3b_attempts = models.IntegerField(initial=0)

    q4a1 = models.StringField(
        label=Constants.q4[0]["label"],
        widget=widgets.RadioSelectHorizontal,
    )
    q4a1_correct = models.BooleanField(initial=False)
    q4a1_attempts = models.IntegerField(initial=0)

    q4a2 = models.StringField(
        label=Constants.q4[1]["label"],
        widget=widgets.RadioSelectHorizontal,
    )
    q4a2_correct = models.BooleanField(initial=False)
    q4a2_attempts = models.IntegerField(initial=0)

    q4a3 = models.StringField(
        label=Constants.q4[2]["label"],
        widget=widgets.RadioSelectHorizontal,
    )
    q4a3_correct = models.BooleanField(initial=False)
    q4a3_attempts = models.IntegerField(initial=0)

    q4b1 = models.StringField(
        label=Constants.q4[3]["label"],
        widget=widgets.RadioSelectHorizontal,
    )
    q4b1_correct = models.BooleanField(initial=False)
    q4b1_attempts = models.IntegerField(initial=0)

    q4b2 = models.StringField(
        label=Constants.q4[4]["label"],
        widget=widgets.RadioSelectHorizontal,
    )
    q4b2_correct = models.BooleanField(initial=False)
    q4b2_attempts = models.IntegerField(initial=0)

    q4b3 = models.StringField(
        label=Constants.q4[5]["label"],
        widget=widgets.RadioSelectHorizontal,
    )

    q4b3_correct = models.BooleanField(initial=False)
    q4b3_attempts = models.IntegerField(initial=0)

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_contribution(self):
        return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_private_contribution(self):
        return sum([p.practice_private_contribution for p in self.in_rounds(1, self.round_number)])

    practice_contribution = models.CurrencyField(min=0, max=10)
    practice_private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()

    participant_vars_dump = models.LongStringField()
