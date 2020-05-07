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
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'progress': 'Game',
            'page_title': 'Energy Conservation Game',
            'current_month': round_month,
            'current_round': self.round_number,
        }

    def before_next_page(self):
        self.group.finalize_group_round_data()



class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    after_all_players_arrive = 'finalize_group_round_data'

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

# FAKE WAITING ROOM
# NOTE: CANNOT USE THE WORD 'FAKE'
# AS IT SHOWS IN THE UP URL
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
        player_total_contrib = self.player.participant.vars["player_total_contrib"]
        player_withheld = self.player.withheld
        group_round_total = self.session.vars["group_round_contrib_total"]
        game_total_contrib = self.session.vars["game_total_contrib"]
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
            "avg_contrib": self.group.group_round_avg,
            "total_players": Constants.game_players,
            "group_round_withholdings": self.session.vars["group_withholdings"],
            "group_total_witheld": c(self.session.vars["group_round_witheld_total"]),
            'group_round_contributions': c(group_round_total - player_contrib),
            'group_total_contributions': c(game_total_contrib - player_total_contrib),
            "player_past_contributions": self.player.participant.vars["player_contributions"],
            "player_past_witholdings": self.player.participant.vars["player_witholdings"],
            "player_total_witheld": c(self.player.participant.vars["player_total_witheld"]),
            "player_contrib_total": c(player_total_contrib),
        }
        return templatevars



class FinalWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    after_all_players_arrive = 'finalize_group_game_data'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



class Congrats(Page):
    form_model = 'player'
    form_fields = [
        'email',
    ]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        game_total_contrib = self.session.vars["game_total_contrib"]
        carbonfund_total = game_total_contrib
        carbon_offset = self.player.tokens_to_dollars(carbonfund_total)
        lbs_reduced = int(game_total_contrib / 10 * 22)
        return {
            'progress': 'Game',
            'current_round': index,
            'current_month': round_month,
            'page_title': 'Your Group\'s Air Pollution Reduction Result',
            'lbs': str(lbs_reduced) + " lbs",
            'amount': carbon_offset,
        }


    def before_next_page(self):
        self.group.finalize_group_game_data()



class FinalResults(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        quiz_bonus = self.player.participant.vars["quiz_bonus"]
        game_total_contrib = self.group.game_total_contrib
        player_contributed = self.player.total_contributed
        player_withheld = self.player.total_witheld
        carbonfund_total = self.group.carbonfund_total
        participation_pay = Constants.participation_pay

        if game_total_contrib >= Constants.group_goal:
            result_message = 'Congratulations, you met the 60% group energy conservation goal of 900 energy tokens.'
            goal_meet = True
            bonus_tokens = int(game_total_contrib * 2 / 25)
        else:
            result_message = 'Sorry, you did not meet the 60% group energy conservation goal of 900 energy tokens.'
            goal_meet = False
            bonus_tokens = 0

        player_contributed_usd = self.player.tokens_to_dollars(player_contributed)
        game_total_usd = self.player.tokens_to_dollars(game_total_contrib)
        quiz_bonus_usd = self.player.tokens_to_dollars(quiz_bonus)
        bonus_tokens_usd = self.player.tokens_to_dollars(bonus_tokens)
        player_withheld_usd = self.player.tokens_to_dollars(player_withheld)
        participation_pay_usd = self.player.tokens_to_dollars(participation_pay)
        carbonfund_total_usd = self.player.tokens_to_dollars(carbonfund_total)

        return {
            'page_title': 'Final Game Result',
            'progress': 'Game',
            'result_message': result_message,
            "goal_meet": goal_meet,
            "game_total_contrib": c(game_total_contrib),
            "game_total_usd": game_total_usd,
            'bonus_tokens': c(bonus_tokens),
            'bonus_tokens_usd': bonus_tokens_usd,
            'quiz_bonus': c(quiz_bonus),
            'quiz_bonus_usd': quiz_bonus_usd,
            'player_withheld': c(player_withheld),
            'player_withheld_usd': player_withheld_usd,
            'player_contributed': c(player_contributed),
            'player_contributed_usd': player_contributed_usd,
            'carbonfund_total': c(carbonfund_total),
            'carbonfund_total_usd': carbonfund_total_usd,
            'participation_pay_usd': participation_pay_usd,
            "total_pay": quiz_bonus_usd + player_withheld_usd + participation_pay_usd + bonus_tokens_usd,
        }



page_sequence = [
    Game,
    # ResultsWaitPage,
    WaitRoom,
    Results,
    # FinalWaitPage,
    Congrats,
    FinalResults,
]
