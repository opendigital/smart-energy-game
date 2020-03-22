import random
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
        return self.round_number >= 1

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'progress': 'Game',
            'page_title': 'Energy Game',
            'current_month': round_month,
            'current_round': self.round_number,
        }


class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    def is_displayed(self):
        return self.round_number >= 1

    def before_next_page(self):
        self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
        self.player.participant.vars['total_witheld'] = self.player.participant.vars['total_witheld'] + self.player.withheld
        self.player.participant.vars['total_contributed'] = self.player.participant.vars['total_contributed'] + self.player.contributed

    def after_all_players_arrive(self):
        self.group.set_bots()
        self.group.set_payoffs()
        self.group.set_total_contribution()



class Results(Page):
    def is_displayed(self):
        return self.round_number >= 1

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        group_round_total = self.session.vars["round_total"]
        player_contributed = self.player.contributed
        game_total = self.session.vars["game_total"]
        group_goal = Constants.group_goal
        percent_complete = str("%.2f" % round(float(100 * game_total / group_goal),2))
        templatevars = {
            "avg_contrib": self.group.group_round_avg,
            "group_goal": group_goal,
            "current_month": round_month,
            "percent_complete": percent_complete,
            "game_total": game_total,
            "page_title":               "Energy Game Results",
            "progress":                 "Game",
            "total_players":            Constants.game_players,
            "player_contributed":       player_contributed,
            "player_withheld":          self.player.withheld,
            "current_round":            self.round_number,
            "round_sums":               self.session.vars["round_sums"],
            "group_round_total":        group_round_total,
            "group_round_withholdings": self.session.vars["round_withholdings"],
            "group_total_withheld":     self.session.vars["total_withheld"],
            'group_round_contributions': (group_round_total - player_contributed),
            "player_past_contributions":self.player.participant.vars["contributions"],
            "player_past_witholdings":  self.player.participant.vars["witholdings"],
            "player_total_witheld":     self.player.participant.vars["total_witheld"],
            "player_total_contributed": self.player.participant.vars["total_contributed"],
        }
        self.player.print_round_results(templatevars)
        self.group.print_round_bot_contributions()
        return templatevars


class Congrats(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        game_total = self.session.vars["game_total"]
        if game_total >= Constants.group_goal:
            game_bonus = game_total
        else:
            game_bonus = 0;
        carbonfund_total = game_bonus + game_total

        return {
            'progress': 'Game',
            'current_round': index,
            'current_month': round_month,
            'page_title': 'Your Group\'s Air Pollution Reduction Result',
            'lbs': str(game_total/10*22).split(" ")[0] + " lbs",
            'amount': self.group.tokens_to_dollars(carbonfund_total),
        }




class FinalResults(Page):

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        quiz_bonus = self.player.participant.vars["quiz_bonus"]
        game_total = self.session.vars["game_total"]
        player_withheld = self.player.participant.vars["total_witheld"]

        if game_total >= Constants.group_goal:
            result_message = 'Congratulations, you met the 60% group energy conservation goal of 900 energy tokens.'
            result_message_classes = '  '
            goal_meet = True
            bonus_tokens = game_total
        else:
            result_message = 'Sorry, you did not meet the 60% group energy conservation goal of 900 energy tokens.'
            goal_meet = False
            bonus_tokens = 0

        game_total_usd = self.group.tokens_to_dollars(game_total)
        quiz_bonus_usd = self.group.tokens_to_dollars(quiz_bonus)
        bonus_tokens_usd = self.group.tokens_to_dollars(bonus_tokens)
        player_withheld_usd = self.group.tokens_to_dollars(player_withheld)
        participation_pay_usd = self.group.tokens_to_dollars(Constants.participation_pay)
        carbonfund_total = game_total + bonus_tokens
        self.group.set_carbonfund_total(carbonfund_total)

        return {
            'page_title': 'Final Game Result',
            'progress': 'Game',
            'current_round': index,
            'current_month': round_month,
            'result_message': result_message,
            "goal_meet": goal_meet,
            "game_total": c(game_total),
            "game_total_usd": game_total_usd,
            'bonus_tokens': c(bonus_tokens),
            'bonus_tokens_usd': bonus_tokens_usd,
            'quiz_bonus': c(quiz_bonus),
            'quiz_bonus_usd': quiz_bonus_usd,
            'player_withheld': c(player_withheld),
            'player_withheld_usd': player_withheld_usd,
            'carbonfund_total': c(carbonfund_total),
            'participation_pay_usd': participation_pay_usd,
            'carbonfund_total_usd': game_total_usd + bonus_tokens_usd,
            "total_pay": quiz_bonus_usd + player_withheld_usd + participation_pay_usd,
        }


    def before_next_page(self):
        self.player.finalize_game_data()


page_sequence = [
    Game,
    ResultsWaitPage,
    Results,
    Congrats,
    FinalResults,
]
