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
    num_actual_rounds = 6
    game_tokens = 10
    game_rounds = 6
    game_players = 25
    game_goal = 900
    num_rounds = num_actual_rounds + 1
    endowment = c(100)
    group_goal = c(900)
    no_bonus = c(0)

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
