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
    num_rounds = 2

    endowment = c(100)
    multiplier = 2

    group_goal = c(216)
    no_bonus = c(0)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    bonus = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.bonus = self.all_rounds_contribution() * Constants.multiplier / Constants.players_per_group

    # It's used for after-survey queries.
    def all_rounds_contribution(self):
            return sum([g.total_contribution for g in self.in_all_rounds()])

    # It's used for before-survey queries.
    def previous_rounds_contribution(self):
            return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)


class Player(BasePlayer):
    signature = models.StringField()
    contribution = models.CurrencyField(min=0, max=Constants.endowment)

    # Randomized for participant and not for groups.
    question = models.StringField(
        label='Adam’s mother has 3 sons. April, May, and __?',
        widget=widgets.RadioSelect)

    def total_contribution(self):
        return sum([p.contribution for p in self.in_all_rounds()])

    def all_rounds_contribution(self):
        return sum([p.contribution for p in self.in_all_rounds()])

    def previous_rounds_contribution(self):
        return sum([p.contribution for p in self.in_previous_rounds()])

    def all_tokens_left(self):
        return 120 - self.all_rounds_contribution()

    def previous_tokens_left(self):
        return 120 - self.previous_rounds_contribution()

    def others_contribution(self):
        return self.group.total_contribution - self.contribution

    def all_rounds_others_contribution(self):
        return self.group.all_rounds_contribution() - self.total_contribution()

    def remaining_tokens_in_dollars(self):
        return c(self.all_tokens_left()).to_real_world_currency(self.session)

    def payoff_in_dollars(self):
        return self.payoff.to_real_world_currency(self.session)