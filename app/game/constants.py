from otree.api import (
    BaseConstants,
    Currency as c,
)
from random import choice

offset = 3
ROUNDS = 6
PLAYERS = 25

class Constants(BaseConstants):
    def __init__(self):
        self.values = ''

    template_config = dict(
        debug_vars=True,
        debug_jsvars=False
    )

    TESTS_EXPORT_HTML = False
    print_game_result_table = False
    DEBUG_ROUND_DATA = False
    multiplier = 2
    name_in_url = 'energy-game'
    players_per_group = None
    reduction_goal = 60
    token_value = .01
    participation_pay = 50
    GAME_TOKENS = 10
    GAME_ROUND_MIN_TIMEOUT_SECONDS = 1
    GAME_ROUND_MAX_TIMEOUT_SECONDS = 5
    game_rounds = ROUNDS
    game_max_score = 1750
    game_players = PLAYERS
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


    offsets = [[[choice([-offset, offset]), choice([-offset, offset])] for player in range(ROUNDS)]
        for round in range(PLAYERS)]
        # inner num is players_per_group, outer_num is num_rounds
