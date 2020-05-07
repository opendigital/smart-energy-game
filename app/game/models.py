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

    def get_reciprocator_contributions(self, round):
        if round == 1:
            return self.RECIPROCATORS_CONTRIBUTIONS_INIT
        elif round == 2:
            return self.RECIPROCATORS_CONTRIBUTIONS_TEST

    def push_round_contributions(self, round_conributions):
        self.contributions.append(round_conributions)
        print('push_round_contributions')
        print(self.contributions)

    def get_bot_contributions(self):
        return self.contributions

    @staticmethod
    def set_contribution_range(minval, maxval, value):
        return min(maxval, max(minval, value))


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["player_round_contrib"] = 0
        self.session.vars["player_round_withheld"] = 0
        self.session.vars["bot_contributions"] = []
        self.session.vars["bot_withholdings_totals"] = []
        self.session.vars["bot_round_contributions"] = []
        self.session.vars["bot_round_withholdings"] = []
        self.session.vars["bot_round_contrib_total"] = 0
        self.session.vars["bot_round_witheld_total"] = 0
        self.session.vars["group_round_contrib_total"] = 0
        self.session.vars["group_round_witheld_total"] = 0
        self.session.vars["group_contribution_totals"] = []
        self.session.vars["group_withholdings"] = []
        self.session.vars["game_total_contrib"] = 0
        self.session.vars["game_total_witheld"] = 0

        for p in self.get_players():
            p.participant.vars["player_player_round_contrib"] = 0
            p.participant.vars["player_player_round_withheld"] = 0
            p.participant.vars["player_bot_contributions"] = []
            p.participant.vars["player_bot_withholdings_totals"] = []
            p.participant.vars["player_bot_round_contributions"] = []
            p.participant.vars["player_bot_round_withholdings"] = []
            p.participant.vars["player_bot_round_contrib_total"] = 0
            p.participant.vars["player_bot_round_witheld_total"] = 0
            p.participant.vars["player_group_round_contrib_total"] = 0
            p.participant.vars["player_group_round_witheld_total"] = 0
            p.participant.vars["player_group_contribution_totals"] = []
            p.participant.vars["player_group_withholdings"] = []
            p.participant.vars["player_game_total_contrib"] = 0
            p.participant.vars["player_game_total_witheld"] = 0

            p.participant.vars['player_contributions'] =[]
            p.participant.vars['player_witholdings'] =[]
            p.participant.vars['player_total_witheld'] = 0
            p.participant.vars['player_total_contrib'] = 0
            p.participant.vars["quiz_bonus"] = 0

            if 'quiz_data' in p.participant.vars:
                quiz_data = p.participant.vars
                p.participant.vars["quiz_bonus"] = quiz_data["quiz_bonus"]
            p.init_player()

    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        game_result = [p.game_result for p in self.get_players()]
        bot_contributions = [p.group.bot_contributions for p in self.get_players()]
        player_contribution = [p.contributed for p in self.get_players()]
        return dict(
            payoffs=payoffs,
            bot_contributions=bot_contributions,
            game_result=game_result,
            player_contribution=player_contribution,
        )


class Group(BaseGroup):
    bot_contributions = models.LongStringField()
    bot_round_contrib_total = models.IntegerField()
    bot_round_avg = models.FloatField()

    group_round_contrib_total = models.IntegerField()
    group_round_witheld_total = models.IntegerField()
    group_round_avg = models.FloatField()

    game_total_contrib = models.IntegerField()
    group_game_bonus = models.IntegerField()
    carbonfund_total = models.IntegerField()


    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def dollars_to_carbon(self, value):
        return value * 10 / 22

    def set_carbonfund_total(self):
        self.carbonfund_total = self.game_total_contrib

    def set_bot_round_avg(self, value):
        self.bot_round_avg  = value

    def set_group_round_avg(self, value):
        self.group_round_avg = value

    def get_bot_round_avg(self):
        return self.group_round_avg

    def set_bot_contributions(self):
        bots = Bots()
        player = self.get_players()[0]
        round_number = self.round_number

        cooperator_list = bots.get_cooperator_contributions()
        freerider_list = bots.get_freerider_contributions()

        diff = []
        new_set = []
        trend = ""

        if round_number <= 1:
            reciprocator_list = bots.get_reciprocator_contributions(round_number)
        elif round_number == 2:
            reciprocator_list = bots.get_reciprocator_contributions(round_number)
        else:
            bots_round_n1_contributions = self.session.vars["bot_contributions"][-1]
            player_round_n1 = player.in_round(round_number - 1)
            player_round_n1_contributed = int(player_round_n1.contributed)
            round_n1_sum = player_round_n1_contributed + sum(bots_round_n1_contributions)
            round_n1_avg = float(round_n1_sum / (len(bots_round_n1_contributions) + 1))

            player_round_n1 = player.in_round(self.round_number - 1).contributed
            player_round_n2 = player.in_round(self.round_number - 2).contributed
            bot_round_n1 = self.session.vars["bot_contributions"][-1]
            bot_round_n2 = self.session.vars["bot_contributions"][-2]

            trend = Functions.get_contribution_trend(
                player_round_n1,
                player_round_n2,
                bot_round_n1,
                bot_round_n2,
            )

            prev_reciprocators = bots_round_n1_contributions[:bots.NUM_RECIPROCATORS:]

            rcp_below_avg = []
            rcp_above_avg = []

            for item in prev_reciprocators:
                if item < round_n1_avg:
                    rcp_below_avg.append(item)
                elif item >= round_n1_avg:
                    rcp_above_avg.append(item)
                else:
                    rcp_above_avg.append(item)

            shuffle(rcp_below_avg)
            shuffle(rcp_above_avg)

            reciprocator_changelist = rcp_below_avg[:bots.NUM_RECIPROCATORS_BELOW_AVG] \
                + rcp_above_avg[-bots.NUM_RECIPROCATORS_ABOVE_AVG:]
            diff = []
            new_set = []

            # ----------------------
            # RECIPROCITY NORM RULES: Trend is up/down
            # SOCIAL NORM RULES: value vs group avg
            # ----------------------
            for value in prev_reciprocators:
                delta = " "

                if value in reciprocator_changelist:
                    delta = "."
                    reciprocator_changelist.remove(value)

                    if trend == "up" and value <= round_n1_avg:
                        value = bots.set_contribution_range(0, 10, value + 1)
                        delta = "+"
                    elif trend == "stable" and value <= round_n1_avg:
                        value = bots.set_contribution_range(0, 10, value + 1)
                        delta = "+"
                    elif trend == "down" and value > round_n1_avg:
                        value = bots.set_contribution_range(0, 10, value - 1)
                        delta = "-"
                    else:
                        delta = " "
                        value = 0

                new_set.append(value)
                diff.append(delta)

            reciprocator_list = new_set
            Functions.print_bot_round_result(new_set, diff, trend)

        new_contributions = reciprocator_list + cooperator_list + freerider_list
        self.session.vars["bot_round_contributions"] = new_contributions
        self.session.vars["bot_contributions"].append(new_contributions)
        bots.push_round_contributions(new_contributions)
        self.bot_contributions = str(new_contributions).replace(" ", "")
        self.bot_round_contrib_total = sum(new_contributions)
        self.bot_round_avg = float(self.bot_round_contrib_total / len(new_contributions))


    def set_group_aggregate_data(self):
        round_fixed_sum = Constants.game_players * 10
        player_round_contrib = self.session.vars["player_round_contrib"]

        bot_round_contrib_total = sum(self.session.vars["bot_round_contributions"])
        bot_round_witheld_total = round_fixed_sum - bot_round_contrib_total

        group_round_contrib_total = bot_round_contrib_total + player_round_contrib

        self.group_round_contrib_total = group_round_contrib_total
        self.group_round_avg = round(float(group_round_contrib_total / Constants.game_players), 3)

        self.session.vars["bot_round_contrib_total"] = bot_round_contrib_total
        self.session.vars["group_round_contrib_total"] = group_round_contrib_total
        self.session.vars["group_contribution_totals"].append(group_round_contrib_total)

        self.session.vars["bot_round_witheld_total"] = bot_round_witheld_total
        self.session.vars["bot_withholdings_totals"].append(bot_round_witheld_total)

        total_withheld = self.session.vars["group_round_witheld_total"]
        game_total_contrib = self.session.vars["game_total_contrib"]

        self.session.vars["group_round_witheld_total"] = total_withheld + bot_round_witheld_total
        self.session.vars["game_total_contrib"] = game_total_contrib + group_round_contrib_total
        self.game_total_contrib = game_total_contrib


    def all_rounds_contribution(self):
        player = self.get_players()[0]
        player_in_all_rounds = player.in_all_rounds()
        player_sum = 0

        for i in range(len(player_in_all_rounds)):
            if player_in_all_rounds[i].contributed is not None:
                player_sum += player_in_all_rounds[i].contributed

        group_sum = sum([sum(x) for x in self.session.vars["bot_contributions"]])
        return c(group_sum + player_sum)


    def finalize_group_player_data(self):
        for player in self.get_players():
            player.set_player_round_data()


    def finalize_group_round_data(self):
        self.set_bot_contributions()
        self.finalize_group_player_data()
        self.set_group_aggregate_data()


    def finalize_group_game_data(self):
        self.game_total_contrib = self.session.vars["game_total_contrib"]
        if self.game_total_contrib >= Constants.group_goal:
            self.group_game_bonus = self.game_total_contrib
        else:
            self.group_game_bonus = 0

        self.set_carbonfund_total()

        for player in self.get_players():
            player.set_player_round_name()
            player.finalize_game_player_data()
            player.cleanup_session_variables()

            if Constants.print_game_result_table:
                player.print_player_game_result_table()


class Player(BasePlayer):
    round = models.StringField()
    email = models.StringField(blank=True)
    contributed = models.IntegerField(min=0, max=10)
    withheld = models.IntegerField(min=0, max=10)
    total_contributed = models.IntegerField()
    total_witheld = models.IntegerField()
    contributions = models.LongStringField()
    player_game_bonus = models.FloatField()
    quiz_bonus = models.IntegerField()
    total_payoff = models.CurrencyField()
    game_result = models.LongStringField()

    player_bot_contributions = models.LongStringField()
    player_bot_round_contrib_total = models.IntegerField()
    player_bot_round_avg = models.FloatField()

    player_bot_round_contrib_total = models.IntegerField()
    player_bot_round_witheld_total = models.IntegerField()
    player_bot_round_avg = models.FloatField()

    player_game_total_contrib = models.IntegerField()
    player_group_game_bonus = models.IntegerField()
    player_carbonfund_total = models.IntegerField()


    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_player_round_name(self):
        if self.round_number == Constants.num_rounds:
            round_title = "rZ"
        else:
            round_title = "r" + str(self.round_number)
        self.round = round_title


    def set_player_bot_contributions(self):
        self.participant.vars['player_bot_contributions'] = bots.get_bot_contributions()


    def set_player_round_data(self):
        self.set_player_round_name()
        self.session.vars['player_round_contrib'] = self.contributed
        self.participant.vars['player_contributions'].append(self.contributed)
        self.participant.vars['player_witholdings'].append(self.withheld)

        self.participant.vars['player_witholdings'].append(self.withheld)

        player_total_contrib = sum(self.participant.vars["player_contributions"])
        player_total_witheld = sum(self.participant.vars["player_witholdings"])

        self.participant.vars["player_total_contrib"] = player_total_contrib
        self.participant.vars["player_total_witheld"] = player_total_witheld

        self.payoff = self.withheld


    def init_player(self):
        if 'quiz_data' in self.participant.vars:
            self.quiz_bonus = self.participant.vars["quiz_bonus"]
        else:
            self.quiz_bonus = 0


    def cleanup_session_variables(self):
        self.session.vars["bot_round_contributions"] = []
        self.session.vars["group_round_contrib"] = []




    def finalize_game_player_data(self):
        if self.group.game_total_contrib >= Constants.group_goal:
            self.player_game_bonus = int(self.group.game_total_contrib * Constants.multiplier / Constants.game_players)
        else:
            self.player_game_bonus = 0

        self.contributions = str(self.participant.vars["player_contributions"])
        self.total_contributed = self.participant.vars["player_total_contrib"]
        self.total_witheld = self.participant.vars["player_total_witheld"]

        game_result = {
            'pl.tcontrib': self.participant.vars["player_contributions"],
            'pl.twitheld': self.participant.vars['player_total_witheld'],
            'pl.contributions': self.participant.vars['player_total_contrib'],
            'bonus_quiz': self.participant.vars['quiz_bonus'],
            'bonus_game': self.player_game_bonus,
        }

        total_payoff = self.tokens_to_dollars(self.quiz_bonus) \
            + self.tokens_to_dollars(self.total_witheld) \
            + self.tokens_to_dollars(self.player_game_bonus)

        self.total_payoff = total_payoff
        self.payoff = int(self.player_game_bonus) + int(self.quiz_bonus)
        self.game_result = str(game_result).replace(", ", ",").replace(": ", ":")


    def print_player_game_result_table(self):
        data = {
            "bot_contributions": self.session.vars["bot_contributions"],
            "game_contributions_total": self.session.vars["game_total_contrib"],
            "player_contributions": self.participant.vars["player_contributions"],
            "player_game_bonus" : self.player_game_bonus,
            "player_payoff": self.participant.payoff,
            "player_payoff_plus_partip_fee": self.participant.payoff_plus_participation_fee(),
            "player_quiz_bonus": self.quiz_bonus,
            "player_total_contributed": self.total_contributed,
            "player_total_payoff": self.total_payoff,
            "player_total_witheld": self.total_witheld,
            "player_vars": self.participant.vars,
        }

        Functions.print_game_result_table(data)
