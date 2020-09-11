from random import randint, shuffle
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range
)
from .utils import Utils
from .constants import Constants
from .functions import Functions

Const = Constants
AUTHOR = 'Matt Harris <m@harr.is>'

DOC = """
RCODI Energy Game - Main App
"""

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def dollars_to_carbon(self, value):
        return value * 10 / 22


class Player(BasePlayer):
    email = models.StringField(blank=True)
    survey_consent = models.BooleanField(
        label="",
        choices=[
            [True, 'Yes, I give my permission for the researchers to use my data.'],
            [False, 'No, I do not give permission for the researchers to use my data. Please discard the data you obtained from me.']
        ],
        widget=widgets.RadioSelect
    )
    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def print_player_game_result_table(self):
        total_payoff = \
            self.tokens_to_dollars(self.participant.vars["quiz_bonus"]) \
            + self.tokens_to_dollars(self.participant.vars["survey_payout"]) \
            + self.tokens_to_dollars(self.participant.vars["player_witholdings_total"]) \
            + self.tokens_to_dollars(self.participant.vars["player_game_bonus"])

        data = {
            "bot_contributions": self.participant.vars["player_bots_contributions"],
            "game_contributions_total": self.participant.vars["player_game_total_contrib"],
            "player_contributions": self.participant.vars["player_contributions"],
            "player_total_contributed": sum(self.participant.vars["player_contributions"]),
            "player_game_bonus" : self.participant.vars["player_game_bonus"],
            "player_payoff": self.participant.payoff,
            "player_payoff_plus_partip_fee": self.participant.payoff_plus_participation_fee(),
            "player_quiz_bonus": self.participant.vars["quiz_bonus"],
            "player_total_payoff": total_payoff,
            "player_total_withheld": self.participant.vars["player_witholdings_total"],
            "player_vars": self.participant.vars,
        }

        Functions.print_game_result_table(data)
