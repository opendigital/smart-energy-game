from random import shuffle
import json
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .constants import Constants
from .utils import Utils


class Congrats(Page):
    form_model = 'player'
    form_fields = [
        'email',
    ]

    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        game_total_contrib = self.player.participant.vars["game_total_contrib"]
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
        if Constants.print_game_result_table:
            self.player.print_player_game_result_table()


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number <= Constants.game_rounds

    def vars_for_template(self):
        quiz_bonus = self.player.participant.vars["quiz_bonus"]
        player_contributed = self.participant.vars['player_contributed']
        player_withheld = self.participant.vars['player_witholdings_total']
        game_total_contrib = self.participant.vars['game_total_contrib']
        carbonfund_total = self.participant.vars['carbonfund_total']
        suvery_payoff = self.participant.vars["survey_payout"]
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
        suvery_payoff_usd = self.player.tokens_to_dollars(suvery_payoff)
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
            'suvery_payoff_usd': suvery_payoff_usd,
            'player_withheld': c(player_withheld),
            'player_withheld_usd': player_withheld_usd,
            'player_contributed': c(player_contributed),
            'player_contributed_usd': player_contributed_usd,
            'carbonfund_total': c(carbonfund_total),
            'carbonfund_total_usd': carbonfund_total_usd,
            'participation_pay_usd': participation_pay_usd,
            "total_pay": quiz_bonus_usd + player_withheld_usd + participation_pay_usd + bonus_tokens_usd + suvery_payoff_usd,
        }


class Debriefing(Page):
    form_model = "player"
    form_fields = ["survey_consent"]

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'page_title': "Debriefing",
            'progress': 'End'
        }

page_sequence = [
    Congrats,
    FinalResults,
    Debriefing,
]
