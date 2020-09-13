from random import shuffle
import json
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .constants import Constants
from .utils import Utils


class Game(Page):
    form_model = 'player'
    form_fields = [
        'contributed',
        'withheld'
    ]

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        game_type = self.session.config["game_type"]
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'progress': 'Game',
            'page_title': 'Energy Conservation Game',
            'current_month': round_month,
            'current_round': self.round_number,
            "game_type": game_type,
            "avg_contrib": self.player.participant.vars["player_group_round_contributions_avg"],
            'player_contributed': self.participant.vars['player_round_contributed'],
        }

    def before_next_page(self):
        self.player.set_player_bots_contributions()
        self.player.set_player_round_data()


class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    after_all_players_arrive = 'finalize_group_round_data'

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds


class WaitRoom(Page):
    template_name = './game/waiting-room.html'
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'progress': 'Game',
            'page_title': 'Energy Conservation Game',
            'current_month': round_month,
            'current_round': self.round_number,
        }


class Results(Page):
    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        player_contrib = self.player.contributed
        player_total_contrib = self.player.participant.vars["player_contributions_total"]
        player_withheld = self.player.withheld
        group_round_total = self.player.participant.vars["player_round_contributed_total"]
        game_total_contrib = self.player.participant.vars["player_game_total_contrib"]
        group_goal = Constants.group_goal
        percent_complete = str("%.2f" % round(float(100 * game_total_contrib / group_goal),2))
        templatevars = {
            "progress": "Game",
            "page_title": "Energy Conservation Game",
            "group_goal": group_goal,
            "current_month": round_month,
            "percent_complete": percent_complete,
            "player_contributed": c(player_contrib),
            "player_withheld": c(player_withheld),
            "game_total_contrib": c(game_total_contrib),
            "group_round_total": c(group_round_total),
            "current_round": self.round_number,
            "avg_contrib": self.player.participant.vars["player_group_round_contributions_avg"],
            "total_players": Constants.game_players,
            # "group_round_withholdings": self.player.participant.vars["player_group_withholdings"],
            # "group_total_withheld": c(self.player.participant.vars["player_group_round_withheld_total"]),
            'group_round_contributions': c(group_round_total - player_contrib),
            'group_total_contributions': c(game_total_contrib - player_total_contrib),
            "player_past_contributions": self.player.participant.vars["player_contributions"],
            # "player_past_witholdings": self.player.participant.vars["player_witholdings"],
            "player_total_withheld": c(self.player.participant.vars["player_witholdings_total"]),
            "player_contrib_total": c(player_total_contrib),
        }
        return templatevars



class FinalWaitPage(Page):
    template_name = './game/waiting-room.html'
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    # after_all_players_arrive = 'finalize_group_game_data'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'progress': 'Game',
            'page_title': 'Energy Conservation Game',
            'current_month': round_month,
            'current_round': self.round_number,
        }

    def before_next_page(self):
        self.player.finalize_game_player_data()


page_sequence = [
    Game,
    WaitRoom,
    Results,
    FinalWaitPage,
]
