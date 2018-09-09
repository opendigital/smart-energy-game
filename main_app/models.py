from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Juan Camilo Cardenas Gomez'

doc = """
Solution for training problem
"""


class Constants(BaseConstants):
    name_in_url = 'training_problem'
    players_per_group = 6
    players_without_me = players_per_group - 1
    num_rounds = 14

    endowment = c(100)
    multiplier = 2

    group_goal = c(216)
    no_bonus = c(0)

    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']

    answers = ["3 tokens", "True", "0 tokens", "10 tokens", 1.82, 0.91]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

        for p in self.get_players():
            self.total_random_contribution = p.contribution + p.random_others_contribution
            p.payoff = c(10) - p.contribution

            if self.round_number > 1:
                if Constants.group_goal <= self.all_rounds_contribution() and (self.round_number == Constants.num_rounds/2 or self.round_number == Constants.num_rounds):
                    self.bonus = self.all_rounds_contribution() * Constants.multiplier / Constants.players_per_group
                    p.payoff += self.bonus

    # It's used for after-survey queries.
    def all_rounds_contribution(self):
            if self.round_number <= Constants.num_rounds / 2:
                return sum([g.total_contribution for g in self.in_rounds(1, self.round_number)])
            else:
                return sum([g.total_contribution for g in self.in_rounds(Constants.num_rounds / 2 + 1, self.round_number)])

    #def all_rounds_random_contribution(self):
    #    return sum([g.total_contribution for g in self.in_previous_rounds()])

    # It's used for before-survey queries.
    def previous_rounds_contribution(self):
            return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)


class Player(BasePlayer):
    # QUIZ
    equilibrium_tokens = models.StringField(
        label='',
        widget=widgets.RadioSelectHorizontal
    )
    donation = models.StringField(
        label='',
        widget=widgets.RadioSelect
    )
    max_individual = models.StringField(
        label='What is the individual level of contribution necessary for maximizing own monetary payoff?',
        widget=widgets.RadioSelectHorizontal
    )
    max_group = models.StringField(
        label='What is the individual level of contribution necessary for maximizing monetary earnings for the group?',
        widget=widgets.RadioSelectHorizontal
    )
    bonus_question = models.FloatField()
    tokens_question = models.FloatField()
    expected_contribution = models.IntegerField(min=0, max=120)
    expected_individual = models.IntegerField(min=0, max=120)

    everything_correct = models.BooleanField()

    # POST_SURVEY
    birth = models.IntegerField()
    gender = models.StringField()
    ethnic_group = models.StringField()
    economic_status = models.StringField()
    previous_experiments = models.StringField()
    reliability = models.StringField()

    # Signature is not being stored
    # signature = models.StringField()

    # quiz_tokens = models.CurrencyField(initial=0)

    contribution = models.CurrencyField(min=0, max=10)
    private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()

    repeatQuiz1 = models.BooleanField(initial=True)
    timesInstruction1 = models.IntegerField(initial=0)
    repeatQuiz2 = models.BooleanField(initial=True)
    timesInstruction2 = models.IntegerField(initial=0)
    repeatQuiz3 = models.BooleanField(initial=True)
    timesInstruction3 = models.IntegerField(initial=0)
    repeatQuiz4 = models.BooleanField(initial=True)
    timesInstruction4 = models.IntegerField(initial=0)


    # First row RESULTS
    def all_tokens_left(self):
        return c(120) - self.all_rounds_contribution()

    def previous_tokens_left(self):
        return c(120) - self.previous_rounds_contribution()

    def all_rounds_contribution(self):
        if self.round_number <= Constants.num_rounds/2:
            return sum([p.contribution for p in self.in_rounds(1, self.round_number)])
        else:
            return sum([p.contribution for p in self.in_rounds(Constants.num_rounds/2+1, self.round_number)])

    def all_rounds_private_contribution(self):
        if self.round_number <= Constants.num_rounds/2:
            return sum([p.private_contribution for p in self.in_rounds(1, self.round_number)])
        else:
            return sum([p.private_contribution for p in self.in_rounds(Constants.num_rounds/2+1, self.round_number)])

    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

    def previous_rounds_contribution(self):
        if self.round_number <= Constants.num_rounds/2:
            return sum([p.contribution for p in self.in_rounds(1, self.round_number-1)])
        else:
            return sum([p.contribution for p in self.in_rounds(Constants.num_rounds/2+1, self.round_number-1)])

    def others_contribution(self):
        return sum([p.contribution for p in self.get_others_in_group()])

    def all_rounds_others_contribution(self):
        return sum([p.all_rounds_contribution() for p in self.get_others_in_group()])

    def remaining_tokens_in_dollars(self):
        return c(self.all_tokens_left()).to_real_world_currency(self.session)

    def total_tokens_in_dollars(self):
        return self.remaining_tokens_in_dollars() + self.group.bonus_in_dollars()

    def total_contribution(self):
        if self.round_number <= Constants.num_rounds / 2:
            return sum([p.contribution for p in self.in_rounds(1, self.round_number - 1)])
        else:
            return sum([p.contribution for p in self.in_rounds(Constants.num_rounds / 2 + 1, self.round_number - 1)])

    def check_answers(self):
        if self.equilibrium_tokens == Constants.answers[0] \
                and self.donation == Constants.answers[1] \
                and self.max_individual == Constants.answers[2] \
                and self.max_group == Constants.answers[3] \
                and self.bonus_question == Constants.answers[4] \
                and self.tokens_question == Constants.answers[5]:
            self.everything_correct = True
            return True
        else:
            self.everything_correct = False
            return False

    def is_equilibrium_tokens_correct(self):
        if self.equilibrium_tokens == Constants.answers[0]:
            self.payoff += 5
            self.repeatQuiz1 = False
            # self.quiz_tokens += c(5)
        return self.equilibrium_tokens == Constants.answers[0]

    def is_donation_correct(self):
        if self.donation == Constants.answers[1]:
            self.payoff += 5
            # self.quiz_tokens += c(5)
        return self.donation == Constants.answers[1]

    def is_max_individual_correct(self):
        if self.max_individual == Constants.answers[2]:
            self.payoff += 5
            # self.quiz_tokens += c(5)
        return self.max_individual == Constants.answers[2]

    def is_max_group_correct(self):
        if self.max_group == Constants.answers[3]:
            self.payoff += 5
            # self.quiz_tokens += c(5)
        return self.max_group == Constants.answers[3]

    def is_bonus_question_correct(self):
        if self.bonus_question == Constants.answers[4]:
            self.payoff += 5
            # self.quiz_tokens += c(5)
        return self.bonus_question == Constants.answers[4]

    def is_tokens_question_correct(self):
        if self.tokens_question == Constants.answers[5]:
            self.payoff += 5
            # self.quiz_tokens += c(5)
        return self.tokens_question == Constants.answers[5]

    def display_instructions_again(self):
        display = self.in_round(Constants.num_rounds / 2)
        return display.everything_correct

    def display_instructions(self):
        if self.round_number == 1:
            return True
        elif self.round_number == Constants.num_rounds/2+1:
            return not self.display_instructions_again()
        else:
            return False

    def how_many_good_answers(self):
        counter = 0
        answers = [self.in_round(Constants.num_rounds/2).equilibrium_tokens==Constants.answers[0],
                   self.in_round(Constants.num_rounds/2).donation==Constants.answers[1],
                   self.in_round(Constants.num_rounds/2).max_individual==Constants.answers[2],
                   self.in_round(Constants.num_rounds/2).max_group==Constants.answers[3],
                   self.in_round(Constants.num_rounds/2).bonus_question==Constants.answers[4],
                   self.in_round(Constants.num_rounds/2).tokens_question==Constants.answers[5],
                   self.in_round(Constants.num_rounds).equilibrium_tokens==Constants.answers[0],
                   self.in_round(Constants.num_rounds).donation==Constants.answers[1],
                   self.in_round(Constants.num_rounds).max_individual==Constants.answers[2],
                   self.in_round(Constants.num_rounds).max_group==Constants.answers[3],
                   self.in_round(Constants.num_rounds).bonus_question==Constants.answers[4],
                   self.in_round(Constants.num_rounds).tokens_question==Constants.answers[5],
                   ]
        for answer_is_correct in answers:
            if answer_is_correct:
                counter+=5
        print('@@@ ', counter)

        return c(counter).to_real_world_currency(self.session)

    def total_pay(self):
        return self.group.bonus_in_dollars() + self.remaining_tokens_in_dollars() + c(50).to_real_world_currency(self.session) + self.how_many_good_answers()