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

class Bots:
    NUM_COOPERATORS = 3
    NUM_FREE_RIDERS = 5
    NUM_RECIPROCATORS = 16
    NUM_RECIPROCATORS_ABOVE_AVG = 3
    NUM_RECIPROCATORS_BELOW_AVG = 2

    COOPERATOR_INITIAL_CONTRIBUTIONS = [10, 9, 8]
    FREERIDER_INITIAL_CONTRIBUTIONS = [3, 3, 2, 2, 1]
    RECIPROCATORS_CONTRIBUTIONS_INIT = [8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4]
    RECIPROCATORS_CONTRIBUTIONS_TEST = [8, 9,  10, 9, 8, 7, 7, 7, 5, 6, 6, 6, 5, 4, 5, 4]

    def __init__(self):
        self.contributions = []

    def get_cooperator_contributions(self):
        return self.COOPERATOR_INITIAL_CONTRIBUTIONS

    def get_freerider_contributions(self):
        return self.FREERIDER_INITIAL_CONTRIBUTIONS

    def get_reciprocator_contributions(self, round_number):
        if round_number == 1:
            return self.RECIPROCATORS_CONTRIBUTIONS_INIT
        elif round_number == 2:
            return self.RECIPROCATORS_CONTRIBUTIONS_TEST

    def get_reciprocator_changelist(self, reciprocator_contributions, avg_contribution):
        rcp_below_avg = []
        rcp_above_avg = []

        for item in reciprocator_contributions:
            if item < avg_contribution:
                rcp_below_avg.append(item)
            elif item >= avg_contribution:
                rcp_above_avg.append(item)
            else:
                rcp_above_avg.append(item)

        shuffle(rcp_below_avg)
        shuffle(rcp_above_avg)

        rcp_index_less = rcp_below_avg[:self.NUM_RECIPROCATORS_BELOW_AVG]
        rcp_index_more = rcp_above_avg[-self.NUM_RECIPROCATORS_ABOVE_AVG:]

        return  rcp_index_less + rcp_index_more

    def update_reciprocator_changelist(self, reciprocator_contributions, changelist, trend, avg_contribution):
        diff = []
        new_set = []

        for value in reciprocator_contributions:
            delta = " "

            if value in changelist:
                changelist.remove(value)

                # RECIPROCITY NORM RULE =  Trend is up/down
                # SOCIAL NORM RULE = value vs group avg
                if trend == "up" and value <= avg_contribution:
                    value = self.set_contribution_range(0, 10, value + 1)
                    delta = "+"
                elif trend == "stable" and value <= avg_contribution:
                    value = self.set_contribution_range(0, 10, value + 1)
                    delta = "+"
                elif trend == "down" and value > avg_contribution:
                    value = self.set_contribution_range(0, 10, value - 1)
                    delta = "-"
                else:
                    delta = " "

            new_set.append(value)
            diff.append(delta)

        return {
            "contributions": new_set,
            "diff": diff,
        }


    def push_round_contributions(self, round_conributions):
        self.contributions.append(round_conributions)
        print('push_round_contributions', self.contributions)

    def get_bots_contributions(self):
        return self.contributions

    @staticmethod
    def set_contribution_range(minval, maxval, value):
        return min(maxval, max(minval, value))


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.participant.vars["quiz_bonus"] = 0
            p.participant.vars['player_round_contributed'] = 0
            p.participant.vars['player_contributions'] = []
            p.participant.vars['player_contributions_total'] = 0
            p.participant.vars["player_contribution_totals"] = []
            p.participant.vars['player_witholdings_total'] = 0
            p.participant.vars['player_witholdings'] = []
            p.participant.vars['player_round_withheld'] = 0
            p.participant.vars["player_round_withheld_total"] = []
            p.participant.vars["player_bots_contributions"] = []
            p.participant.vars["player_bots_contributions_total"] = 0
            p.participant.vars["player_bots_witholdings"] = []
            p.participant.vars["player_bots_withholdings_totals"] = []
            p.participant.vars["player_bots_round_contrib_total"] = 0
            p.participant.vars["player_bots_round_contributions"] = []
            p.participant.vars["player_bots_round_withheld_total"] = 0
            p.participant.vars["player_bots_round_withholdings"] = []
            p.participant.vars["player_group_round_contrib_total"] = 0
            p.participant.vars["player_group_round_withheld_total"] = 0
            p.participant.vars["player_group_contribution_totals"] = []
            p.participant.vars["player_group_withholdings"] = []
            p.participant.vars["player_group_round_contributions_avg"] = 0
            p.participant.vars['player_total_contrib'] = 0
            p.participant.vars["player_game_total_contrib"] = 0
            p.participant.vars["player_game_total_withheld"] = 0

            if 'quiz_data' in p.participant.vars:
                quiz_data = p.participant.vars
                p.participant.vars["quiz_bonus"] = quiz_data["quiz_bonus"]

            p.init_player()

    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        game_result = [p.game_result for p in self.get_players()]
        player_contribution = [p.contributed for p in self.get_players()]
        return dict(
            payoffs=payoffs,
            game_result=game_result,
            player_contribution=player_contribution,
        )


class Group(BaseGroup):
    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def dollars_to_carbon(self, value):
        return value * 10 / 22


class Player(BasePlayer):
    player_bots = Bots()
    round = models.StringField()
    contributed = models.IntegerField(min=0, max=10)
    contributions = models.LongStringField()
    player_contributions_total = models.IntegerField()
    withheld = models.IntegerField(min=0, max=10)
    player_witholdings_total = models.IntegerField()
    game_result = models.LongStringField()
    round_avg = models.FloatField()
    player_bots_contributions = models.LongStringField()
    player_bots_round_avg = models.FloatField()
    player_bots_round_contrib_total = models.IntegerField()
    player_bots_round_withheld_total = models.IntegerField()
    player_carbonfund_total = models.IntegerField()
    quiz_bonus = models.IntegerField()
    player_game_bonus = models.IntegerField(initial=0)
    player_game_total_contrib = models.IntegerField(initial=0)
    total_payoff = models.CurrencyField()

    def init_player(self):
        self.participant.vars["player_bots"] = Bots()
        if 'quiz_data' in self.participant.vars:
            self.quiz_bonus = self.participant.vars["quiz_bonus"]
        else:
            self.quiz_bonus = 0

    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_player_round_name(self):
        if self.round_number == Constants.num_rounds:
            round_title = "rZ"
        else:
            round_title = "r" + str(self.round_number)
        self.round = round_title

    def set_player_carbonfund_total(self):
        self.player_carbonfund_total = self.player_game_total_contrib

    def set_player_bots_contributions(self):
        # PLAYER_BOTS SET VALUES LOCAL TO THE SINGLE PLAYER IN THE SESSION
        # THIS IS DIFFERENT FROM A GAME WHERE MULTIPLE PLAYERS SHARE INFO
        # FROM THE SAME GROUP OF BOT PLAYERS

        bots = Bots()
        round_number = self.round_number

        cooperator_list = bots.get_cooperator_contributions()
        freerider_list = bots.get_freerider_contributions()

        trend = ""

        if round_number <= 2:

            reciprocator_list = bots.get_reciprocator_contributions(round_number)
        else:
            player_round_n1 = self.participant.vars['player_contributions'][-1]
            player_round_n2 = self.participant.vars['player_contributions'][-2]

            bots_round_n1_contributions = self.participant.vars["player_bots_contributions"][-1]
            bots_round_n2_contributions = self.participant.vars["player_bots_contributions"][-2]

            prev_round_sum = int(player_round_n1) + sum(bots_round_n1_contributions)
            prev_round_avg = float(prev_round_sum / (len(bots_round_n1_contributions) + 1))


            trend = Functions.get_contribution_trend(
                player_round_n1,
                player_round_n2,
                bots_round_n1_contributions,
                bots_round_n2_contributions,
            )

            prev_reciprocators = bots_round_n1_contributions[:bots.NUM_RECIPROCATORS:]

            reciprocator_changelist = bots.get_reciprocator_changelist(prev_reciprocators, prev_round_avg)

            rcp_data = bots.update_reciprocator_changelist(
                prev_reciprocators,
                reciprocator_changelist,
                trend,
                prev_round_avg,
            )

            if Constants.DEBUG_ROUND_DATA:
                Functions.print_bot_round_result(rcp_data["contributions"], rcp_data["diff"], trend)

            reciprocator_list = rcp_data["contributions"]

        new_contributions = reciprocator_list + cooperator_list + freerider_list

        self.participant.vars["player_bots_round_contributions"] = new_contributions
        self.participant.vars["player_bots_contributions"].append(new_contributions)
        self.player_bots_contributions = str(new_contributions).replace(" ", "")
        self.player_bots_round_contrib_total = sum(new_contributions)
        self.player_bots_round_avg = float(self.player_bots_round_contrib_total / len(new_contributions))


    def set_player_round_data(self):
        self.set_player_round_name()

        round_fixed_sum = Constants.game_players * Constants.GAME_TOKENS
        bots_round_fixed_sum = (Constants.game_players - 1) * Constants.GAME_TOKENS

        self.participant.vars['player_round_contributed'] = self.contributed
        self.participant.vars['player_contributions'].append(self.contributed)
        player_contributions_total = sum(self.participant.vars['player_contributions'])
        self.player_contributions_total = player_contributions_total
        self.participant.vars['player_contributions_total'] = player_contributions_total

        self.participant.vars['player_round_withheld'] = self.withheld
        self.participant.vars['player_witholdings'].append(self.withheld)
        player_witholdings_total = sum(self.participant.vars['player_witholdings'])
        self.player_witholdings_total = player_witholdings_total
        self.participant.vars['player_witholdings_total'] = player_witholdings_total

        self.payoff = self.withheld

        bot_round_contrib_total = sum(self.participant.vars["player_bots_round_contributions"])
        player_round_contributed_total = self.contributed + bot_round_contrib_total
        self.participant.vars["player_round_contributed_total"] = player_round_contributed_total

        # player_bots_contributions = self.participant.vars["player_bots_contributions"]
        # player_bots_contributions_total = Utils.game_round_sum(player_bots_contributions)

        bot_round_withheld_total = round_fixed_sum - bot_round_contrib_total
        group_round_contrib_total = bot_round_contrib_total + self.contributed

        self.participant.vars["player_round_contributed_total"] = group_round_contrib_total
        self.round_avg = round(float(group_round_contrib_total / Constants.game_players), 3)
        self.participant.vars["player_group_round_contributions_avg"] = self.round_avg
        self.participant.vars["player_bots_round_contrib_total"] = bot_round_contrib_total
        self.participant.vars["player_contribution_totals"].append(group_round_contrib_total)
        self.participant.vars["player_bots_round_withheld_total"] = bot_round_withheld_total
        self.participant.vars["player_bots_withholdings_totals"].append(bot_round_withheld_total)

        # total_withheld = self.participant.vars["player_round_withheld_total"]
        game_total_contrib = self.participant.vars["player_game_total_contrib"]

        self.participant.vars["player_round_withheld_total"] = self.withheld + bot_round_withheld_total
        self.participant.vars["player_game_total_contrib"] = game_total_contrib + group_round_contrib_total
        self.player_game_total_contrib = game_total_contrib


    def cleanup_session_variables(self):
        self.participant.vars["player_bots_round_contributions"] = []
        self.participant.vars["player_group_round_contrib"] = []


    def finalize_game_player_data(self):
        self.participant.vars["game_total_contrib"] = self.player_game_total_contrib
        self.participant.vars["carbonfund_total"] = self.player_carbonfund_total
        self.participant.vars["game_total_contrib"] = self.participant.vars["player_game_total_contrib"]
        self.participant.vars["carbonfund_total"] = self.participant.vars["game_total_contrib"]
        self.participant.vars["player_contributed"] = self.participant.vars['player_contributions_total']
        self.participant.vars["total_payoff"] = self.total_payoff
        self.player_game_total_contrib = self.participant.vars["player_game_total_contrib"]

        if self.player_game_total_contrib >= Constants.group_goal:
            self.player_game_bonus = int(self.player_game_total_contrib * Constants.multiplier / Constants.game_players)
        else:
            self.player_game_bonus = 0

        self.participant.vars["player_game_bonus"] = self.player_game_bonus

        self.set_player_carbonfund_total()

        self.contributions = str(self.participant.vars["player_contributions"])
        self.player_contributions_total = self.participant.vars["player_total_contrib"]
        self.player_witholdings_total = self.participant.vars["player_witholdings_total"]
        self.participant.vars["player_withheld"] = self.player_witholdings_total

        self.payoff = int(self.player_game_bonus)

        game_result = {
            'game_type': self.session.config["game_type"],
            'contributions': self.participant.vars["player_contributions"],
            'total_withheld': self.participant.vars['player_witholdings_total'],
            'total_contributed': sum(self.participant.vars['player_contributions']),
            'bonus_quiz': self.participant.vars['quiz_bonus'],
            'bonus_game': self.player_game_bonus,
        }

        self.game_result = str(game_result).replace(", ", ",").replace(": ", ":")

    def print_player_game_result_table(self):
        data = {
            "bot_contributions": self.participant.vars["player_bots_contributions"],
            "game_contributions_total": self.participant.vars["player_game_total_contrib"],
            "player_contributions": self.participant.vars["player_contributions"],
            "player_total_contributed": sum(self.participant.vars["player_contributions"]),
            "player_game_bonus" : self.player_game_bonus,
            "player_payoff": self.participant.payoff,
            "player_payoff_plus_partip_fee": self.participant.payoff_plus_participation_fee(),
            "player_quiz_bonus": self.quiz_bonus,
            "player_total_payoff": self.total_payoff,
            "player_total_withheld": self.player_witholdings_total,
            "player_vars": self.participant.vars,
        }

        Functions.print_game_result_table(data)
