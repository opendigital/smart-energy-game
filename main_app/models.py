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
    players_per_group = 3
    players_without_me = players_per_group - 1
    num_rounds = 24

    endowment = c(100)
    multiplier = 2

    group_goal = c(216)
    no_bonus = c(0)

    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']

    answers = ["3 tokens", "The total tokens in the House Conservation Fund x $.01 to convert the energy tokens into dollars.", "0 tokens", "10 tokens", 1.82, 0.91]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

        for p in self.get_players():
            p.payoff = c(10) - p.contribution

            if self.round_number > 1:
                if Constants.group_goal <= self.all_rounds_contribution() and (self.round_number == Constants.num_rounds/2 or self.round_number == Constants.num_rounds):
                    self.bonus = self.all_rounds_contribution() * Constants.multiplier / Constants.players_per_group
                    p.payoff += self.bonus

            # if p.tokens is None or self.round_number == 13:
            #     p.tokens = c(120)
            #     self.set_payoffs()
            # elif self.round_number == 12 or self.round_number == 24:
            #     print(p.tokens)
            #     p.payoff += p.tokens.to_real_world_currency(self.session)
            #     if self.all_rounds_contribution() >= Constants.group_goal:
            #         p.bonus_tokens = self.all_rounds_contribution()
            #         p.payoff += self.bonus_in_dollars()/Constants.players_per_group
            # else:
            #     p.tokens -= p.contribution


    # It's used for after-survey queries.
    def all_rounds_contribution(self):
            # return sum([g.total_contribution for g in self.in_all_rounds()])

            if self.round_number <= Constants.num_rounds / 2:
                return sum([g.total_contribution for g in self.in_rounds(1, self.round_number)])
            else:
                return sum([g.total_contribution for g in self.in_rounds(Constants.num_rounds / 2 + 1, self.round_number)])

    # It's used for before-survey queries.
    def previous_rounds_contribution(self):
            return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)

    # def set_question_payoff(self, number):
    #     for p in self.get_players():
    #         p.in_round(Constants.num_rounds/2).is_



class Player(BasePlayer):
    # QUIZ
    equilibrium_tokens = models.StringField(
        label='At minimum, how many tokens will each player have to invest into the House Conservation Fund in each round on average to meet the group conservation goal of 216 energy tokens?',
        widget=widgets.RadioSelectHorizontal
    )
    donation = models.StringField(
        label=' Assuming the contributions to the House Conservation Fund meet the group conservation goal of 216, what is the total donation given to Carbonfund.org to reduce air pollution?',
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

    trial_tokens = models.CurrencyField()
    game_tokens = models.CurrencyField()

    quiz_tokens = models.CurrencyField(initial=0)

    contribution = models.CurrencyField(min=0, max=Constants.endowment)

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


    #
    def initialize_tokens(self):
        self.tokens = c(120)

    def check_answers(self):
        if self.is_equilibrium_tokens_correct() and self.is_donation_correct() and self.is_max_group_correct() and self.is_max_individual_correct() and self.is_bonus_question_correct() and self.is_tokens_question_correct():
            self.everything_correct = True
            return True
        else:
            self.everything_correct = False
            return False

    def is_equilibrium_tokens_correct(self):
        if self.equilibrium_tokens == Constants.answers[0]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.equilibrium_tokens == Constants.answers[0]

    def is_donation_correct(self):
        if self.donation == Constants.answers[1]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.donation == Constants.answers[1]

    def is_max_individual_correct(self):
        if self.max_individual == Constants.answers[2]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.max_individual == Constants.answers[2]

    def is_max_group_correct(self):
        if self.max_group == Constants.answers[3]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.max_group == Constants.answers[3]

    def is_bonus_question_correct(self):
        if self.bonus_question == Constants.answers[4]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.bonus_question == Constants.answers[4]

    def is_tokens_question_correct(self):
        if self.tokens_question == Constants.answers[5]:
            self.payoff += 5
            self.quiz_tokens += c(5)
        return self.tokens_question == Constants.answers[5]

    def display_instructions_again(self):
        display = self.in_round(Constants.num_rounds / 2)
        return display.everything_correct

    def display_instructions(self):
        if self.round_number == 1:
            return True
        elif self.round_number == Constants.num_rounds/2+1:
            print('@@@ everything_correct? ', self.display_instructions_again())
            return not self.display_instructions_again()
        else:
            return False

    def how_many_good_answers(self):
        counter = 0
        if self.in_round(Constants.num_rounds/2).is_equilibrium_tokens_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds/2).is_donation_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds/2).is_max_individual_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds/2).is_max_group_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds/2).is_bonus_question_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds/2).is_tokens_question_correct():
            counter+=1
        if self.in_round(Constants.num_rounds).is_equilibrium_tokens_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds).is_donation_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds).is_max_individual_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds).is_max_group_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds).is_bonus_question_correct():
            counter+=1
        elif self.in_round(Constants.num_rounds).is_tokens_question_correct():
            counter+=1

        return c(counter).to_real_world_currency(self.session)

    def total_pay(self):
        return self.group.bonus_in_dollars() + self.remaining_tokens_in_dollars() + c(50).to_real_world_currency(self.session) + self.how_many_good_answers()