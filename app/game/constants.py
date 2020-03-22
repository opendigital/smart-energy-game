from otree.api import (
    BaseConstants,
    Currency as c,
)


class Constants(BaseConstants):
    def __init__(self):
        self.values = ''

    template_config = dict(
        debug_vars=True,
        debug_jsvars=False
    )

    multiplier = 2
    name_in_url = 'energy-game'
    players_per_group = None
    reduction_goal = 60
    token_value = .01
    participation_pay = token_value * 50
    game_tokens = 10
    game_rounds = 6
    game_max_score = 1750
    game_players = 25
    game_goal = 900
    num_rounds = 6
    endowment = 100
    group_goal = 900

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
