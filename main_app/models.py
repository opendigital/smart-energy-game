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
    num_rounds = 13

    endowment = c(100)
    multiplier = 2

    group_goal = c(216)
    no_bonus = c(0)

    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']

    answers = ["3 tokens", "True", "True", "True","$1.08","$1.00","$2.08","$1.08","$0.00","$1.08"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

        for p in self.get_players():
            if self.total_random_contribution:
                self.total_random_contribution = p.contribution + p.random_others_contribution

            p.payoff = c(10) - p.contribution

            if self.round_number == 13:
                if Constants.group_goal <= self.all_rounds_contribution() and (self.round_number == Constants.num_rounds/2 or self.round_number == Constants.num_rounds):
                    self.bonus = self.all_rounds_contribution() * Constants.multiplier / Constants.players_per_group
                    p.payoff += self.bonus

    # It's used for after-survey queries.
    def all_rounds_contribution(self):
        return sum([g.total_contribution for g in self.in_rounds(2, self.round_number)])

    # It's used for before-survey queries.
    def previous_rounds_contribution(self):
            return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)


class Player(BasePlayer):
    # PRACTICE AND REAL GAME
    contribution = models.CurrencyField(min=0, max=10)
    practice_contribution = models.CurrencyField(min=0, max=10)
    private_contribution = models.CurrencyField(min=0, max=10)
    practice_private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()

    # QUIZ
    Q1 = models.StringField(label='', widget=widgets.RadioSelectHorizontal)
    Q2 = models.StringField(label='', widget=widgets.RadioSelect)
    Q3a = models.StringField(label='', widget=widgets.RadioSelectHorizontal)
    Q3b = models.StringField(label='', widget=widgets.RadioSelectHorizontal)

    answerQ4a1 = models.StringField()
    answerQ4a2 = models.StringField()
    answerQ4a3 = models.StringField()
    answerQ4b1 = models.StringField()
    answerQ4b2 = models.StringField()
    answerQ4b3 = models.StringField()

    repeatQuiz1 = models.BooleanField(initial=False)
    timesInstruction1 = models.IntegerField(initial=0)
    repeatQuiz2 = models.BooleanField(initial=False)
    timesInstruction2 = models.IntegerField(initial=0)
    repeatQuiz3a = models.BooleanField(initial=False)
    timesInstruction3a = models.IntegerField(initial=0)
    repeatQuiz3b = models.BooleanField(initial=False)
    timesInstruction3b = models.IntegerField(initial=0)
    repeatQuiz4 = models.BooleanField(initial=False)
    timesInstruction4 = models.IntegerField(initial=0)

    doItOnce = models.BooleanField(initial=True)
    doItOnce2 = models.BooleanField(initial=True)
    doItOnce3 = models.BooleanField(initial=True)
    doItOnce4 = models.BooleanField(initial=True)

    # POST_SURVEY
    birth = models.IntegerField()
    gender = models.StringField()
    ethnic_group = models.StringField()
    economic_status = models.StringField()
    previous_experiments = models.StringField()
    reliability = models.StringField()

    # WILD METHODS
    def all_tokens_left(self):
        return c(120) - self.all_rounds_contribution()

    def previous_tokens_left(self):
        return c(120) - self.previous_rounds_contribution()

    def all_rounds_contribution(self):
        return sum([p.contribution for p in self.in_rounds(2, self.round_number)])

    def all_rounds_practice_contribution(self):
        return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_private_contribution(self):
        return sum([p.practice_private_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_private_contribution(self):
        return sum([p.private_contribution for p in self.in_rounds(2, self.round_number)])

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
        if self.Q1 == Constants.answers[0] \
                and self.Q2 == Constants.answers[1] \
                and self.Q3a == Constants.answers[2] \
                and self.Q3b == Constants.answers[3]:
            self.everything_correct = True
            return True
        else:
            self.everything_correct = False
            return False

    def is_equilibrium_tokens_correct(self):
        if self.Q1 == Constants.answers[0] and self.doItOnce4:
            self.payoff += 5
            self.doItOnce4 = False
        return self.Q1 == Constants.answers[0]

    def is_donation_correct(self):
        if self.Q2 == Constants.answers[1] and self.doItOnce3:
            self.doItOnce3 = False
            self.payoff += 5
        return self.Q2 == Constants.answers[1]

    def is_both_Examples_right(self):
        if self.Q3a == Constants.answers[2] and self.Q3b == Constants.answers[3] and self.doItOnce :
            self.payoff += 5
            self.doItOnce = False
        return self.Q3a == Constants.answers[2] and self.Q3b == Constants.answers[3]

    def is_all_values_right(self):
        if self.doItOnce2 and self.answerQ4a1 == Constants.answers[4] and self.answerQ4a2 == Constants.answers[5] and self.answerQ4a3 == Constants.answers[6] and self.answerQ4b1 == Constants.answers[7] and self.answerQ4b2 == Constants.answers[8] and self.answerQ4b3 == Constants.answers[9]:
            self.payoff += 5
            self.doItOnce2 = False
        return self.answerQ4a1 == Constants.answers[4] and self.answerQ4a2 == Constants.answers[5] and self.answerQ4a3 == Constants.answers[6] and self.answerQ4b1 == Constants.answers[7] and self.answerQ4b2 == Constants.answers[8] and self.answerQ4b3 == Constants.answers[9]

    def is_max_individual_correct(self):
        return self.Q3a == Constants.answers[2]

    def is_max_group_correct(self):
        return self.Q3b == Constants.answers[3]

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
        answers = [
                   self.in_round(2).Q1 == Constants.answers[0],
                   self.in_round(2).Q2 == Constants.answers[1],
                   self.is_both_Examples_right(),
                   self.is_all_values_right(),
                   ]
        for answer_is_correct in answers:
            if answer_is_correct:
                counter+=5
        print('@@@ ', counter)

        return c(counter).to_real_world_currency(self.session)

    def total_pay(self):
        return self.group.bonus_in_dollars() + self.remaining_tokens_in_dollars() + c(50).to_real_world_currency(self.session) + self.how_many_good_answers()