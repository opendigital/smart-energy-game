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

    TESTS_EXPORT_HTML = True
    multiplier = 2
    print_game_result_table = True
    name_in_url = 'energy-game'
    players_per_group = None
    reduction_goal = 60
    token_value = .01
    participation_pay = 50
    game_tokens = 10
    game_rounds = 6
    game_max_score = 1750
    game_players = 25
    game_goal = 900
    num_rounds = game_rounds + 1
    endowment = 100
    group_goal = 900

    game_progress = [
        1,
        2,
        3,
        4,
        5,
        6,
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
