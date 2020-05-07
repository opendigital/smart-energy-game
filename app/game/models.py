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
                    value = 0

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
        # self.session.vars["player_round_contrib"] = 0
        # self.session.vars["player_round_withheld"] = 0
        # self.session.vars["bots_contributions"] = []
        # self.session.vars["bot_withholdings_totals"] = []
        # self.session.vars["bot_round_contributions"] = []
        # self.session.vars["bot_round_withholdings"] = []
        # self.session.vars["bot_round_contrib_total"] = 0
        # self.session.vars["bot_round_withheld_total"] = 0
        # self.session.vars["group_round_contrib_total"] = 0
        # self.session.vars["group_round_withheld_total"] = 0
        # self.session.vars["group_contribution_totals"] = []
        # self.session.vars["group_withholdings"] = []
        # self.session.vars["game_total_contrib"] = 0
        # self.session.vars["game_total_withheld"] = 0

        for p in self.get_players():
            p.participant.vars['player_round_contributed'] = 0
            p.participant.vars['player_contributions'] = []
            p.participant.vars['player_contributions_total'] = 0

            p.participant.vars['player_round_withheld'] = 0
            p.participant.vars['player_witholdings'] = []
            p.participant.vars['player_witholdings_total'] = 0

            p.participant.vars["player_bots_contributions"] = []
            p.participant.vars["player_bots_contributions_total"] = 0

            p.participant.vars["player_bots_witholdings"] = []

            p.participant.vars["player_bots_withholdings_totals"] = []
            p.participant.vars["player_bots_round_contributions"] = []

            p.participant.vars["player_bots_round_withholdings"] = []
            p.participant.vars["player_bots_round_contrib_total"] = 0
            p.participant.vars["player_bots_round_withheld_total"] = 0
            p.participant.vars["player_group_round_contrib_total"] = 0
            p.participant.vars["player_group_round_withheld_total"] = 0

            p.participant.vars["player_group_contribution_totals"] = []
            p.participant.vars["player_contribution_totals"] = []

            p.participant.vars["player_group_withholdings"] = []
            p.participant.vars["player_round_withheld_total"] = []

            p.participant.vars["player_group_round_contributions_avg"] = 0
            p.participant.vars["player_game_total_contrib"] = 0
            p.participant.vars["player_game_total_withheld"] = 0


            p.participant.vars['player_total_withheld'] = 0
            p.participant.vars['player_total_contrib'] = 0
            p.participant.vars["quiz_bonus"] = 0

            if 'quiz_data' in p.participant.vars:
                quiz_data = p.participant.vars
                p.participant.vars["quiz_bonus"] = quiz_data["quiz_bonus"]
            p.init_player()

    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        game_result = [p.game_result for p in self.get_players()]
        bots_contributions = [p.group.bots_contributions for p in self.get_players()]
        player_contribution = [p.contributed for p in self.get_players()]
        return dict(
            payoffs=payoffs,
            bots_contributions=bots_contributions,
            game_result=game_result,
            player_contribution=player_contribution,
        )


class Group(BaseGroup):
    bots_contributions = models.LongStringField()
    bot_round_contrib_total = models.IntegerField()
    bot_round_avg = models.FloatField()

    group_round_contrib_total = models.IntegerField()
    group_round_withheld_total = models.IntegerField()
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
        self.bot_round_avg = value

    def set_group_round_avg(self, value):
        self.group_round_avg = value

    def get_bot_round_avg(self):
        return self.group_round_avg

    def set_bots_contributions(self):
        bots = Bots()
        player = self.get_players()[0]
        round_number = self.round_number

        cooperator_list = bots.get_cooperator_contributions()
        freerider_list = bots.get_freerider_contributions()

        trend = ""

        if round_number <= 2:
            reciprocator_list = bots.get_reciprocator_contributions(round_number)
        else:
            player_round_n1 = player.in_round(round_number - 1)
            player_round_n2 = player.in_round(round_number - 2)

            bots_round_n1_contributions = self.session.vars["bots_contributions"][-1]
            bots_round_n2_contributions = self.session.vars["bots_contributions"][-2]

            prev_round_sum = int(player_round_n1.contributed) + sum(bots_round_n1_contributions)
            prev_round_avg = float(prev_round_sum / (len(bots_round_n1_contributions) + 1))


            trend = Functions.get_contribution_trend(
                player_round_n1.contributed,
                player_round_n2.contributed,
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

            Functions.print_bot_round_result(rcp_data["contributions"], rcp_data["diff"], trend)

            reciprocator_list = rcp_data["contributions"]

        new_contributions = reciprocator_list + cooperator_list + freerider_list
        self.session.vars["bot_round_contributions"] = new_contributions
        self.session.vars["bots_contributions"].append(new_contributions)
        bots.push_round_contributions(new_contributions)
        self.bots_contributions = str(new_contributions).replace(" ", "")
        self.bot_round_contrib_total = sum(new_contributions)
        self.bot_round_avg = float(self.bot_round_contrib_total / len(new_contributions))


    def set_group_aggregate_data(self):
        round_fixed_sum = Constants.game_players * 10
        player_round_contrib = self.session.vars["player_round_contrib"]

        bot_round_contrib_total = sum(self.session.vars["bot_round_contributions"])
        bot_round_withheld_total = round_fixed_sum - bot_round_contrib_total

        group_round_contrib_total = bot_round_contrib_total + player_round_contrib

        self.group_round_contrib_total = group_round_contrib_total
        self.group_round_avg = round(float(group_round_contrib_total / Constants.game_players), 3)

        self.session.vars["bot_round_contrib_total"] = bot_round_contrib_total
        self.session.vars["group_round_contrib_total"] = group_round_contrib_total
        self.session.vars["group_contribution_totals"].append(group_round_contrib_total)

        self.session.vars["bot_round_withheld_total"] = bot_round_withheld_total
        self.session.vars["bot_withholdings_totals"].append(bot_round_withheld_total)

        total_withheld = self.session.vars["group_round_withheld_total"]
        game_total_contrib = self.session.vars["game_total_contrib"]

        self.session.vars["group_round_withheld_total"] = total_withheld + bot_round_withheld_total
        self.session.vars["game_total_contrib"] = game_total_contrib + group_round_contrib_total
        self.game_total_contrib = game_total_contrib


    def all_rounds_contribution(self):
        player = self.get_players()[0]
        player_in_all_rounds = player.in_all_rounds()
        player_sum = 0

        for i in range(len(player_in_all_rounds)):
            if player_in_all_rounds[i].contributed is not None:
                player_sum += player_in_all_rounds[i].contributed

        group_sum = sum([sum(x) for x in self.session.vars["bots_contributions"]])
        return c(group_sum + player_sum)


    def finalize_group_round_data(self):
        print("finalize_group_round_data")
        self.set_bots_contributions()
        self.set_group_aggregate_data()
        self.finalize_group_player_data()

    def finalize_group_player_data(self):
        print("finalize_group_player_data")
        for player in self.get_players():
            player.set_player_round_data()

    def finalize_group_game_data(self):
        print("finalize_group_game_data")
        self.game_total_contrib = self.session.vars["game_total_contrib"]
        if self.game_total_contrib >= Constants.group_goal:
            self.group_game_bonus = self.game_total_contrib
        else:
            self.group_game_bonus = 0

        self.set_carbonfund_total()
        # for player in self.get_players():
        #     player.set_player_round_name()
        #     player.finalize_game_player_data()
        #     player.cleanup_session_variables()
        #
        #     if Constants.print_game_result_table:
        #         player.print_player_game_result_table()


class Player(BasePlayer):
    player_bots = Bots()
    round = models.StringField()
    email = models.StringField(blank=True)

    contributed = models.IntegerField(min=0, max=10)
    withheld = models.IntegerField(min=0, max=10)
    total_contributed = models.IntegerField()
    player_total_withheld = models.IntegerField()
    contributions = models.LongStringField()

    player_game_bonus = models.FloatField()
    round_avg = models.FloatField()
    quiz_bonus = models.IntegerField()
    total_payoff = models.CurrencyField()
    game_result = models.LongStringField()

    player_bots_contributions = models.LongStringField()
    player_bots_round_contrib_total = models.IntegerField()
    player_bots_round_withheld_total = models.IntegerField()
    player_bots_round_avg = models.FloatField()

    player_game_total_contrib = models.IntegerField(initial=0)
    player_game_bonus = models.IntegerField()
    player_carbonfund_total = models.IntegerField()

    def init_player(self):
        print('init player')
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
            print("player_contributions", self.participant.vars['player_contributions'])
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
        self.participant.vars['player_contributions_total'] = player_contributions_total

        self.participant.vars['player_round_withheld'] = self.withheld
        self.participant.vars['player_witholdings'].append(self.withheld)
        self.player_total_withheld = sum(self.participant.vars['player_witholdings'])
        self.participant.vars['player_witholdings_total'] = self.player_total_withheld
        self.payoff = self.withheld

        player_round_contributed_total = self.contributed + sum(self.participant.vars["player_bots_round_contributions"])
        self.participant.vars["player_round_contributed_total"] = player_round_contributed_total
        player_bots_contributions = self.participant.vars["player_bots_contributions"]
        player_bots_contributions_total = Utils.game_round_sum(player_bots_contributions)

        bot_round_contrib_total = sum(self.participant.vars["player_bots_round_contributions"])
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

        print("finalize_group_game_data")
        self.player_game_total_contrib = self.participant.vars["player_game_total_contrib"]
        if self.player_game_total_contrib >= Constants.group_goal:
            self.player_game_bonus = self.player_game_total_contrib
        else:
            self.player_game_bonus = 0

        self.set_player_carbonfund_total()

        if self.player_game_total_contrib >= Constants.group_goal:
            self.player_game_bonus = int(self.player_game_total_contrib * Constants.multiplier / Constants.game_players)
        else:
            self.player_game_bonus = 0

        self.contributions = str(self.participant.vars["player_contributions"])
        self.total_contributed = self.participant.vars["player_total_contrib"]
        self.player_total_withheld = self.participant.vars["player_total_withheld"]

        game_result = {
            'pl.tcontrib': self.participant.vars["player_contributions"],
            'pl.twithheld': self.participant.vars['player_total_withheld'],
            'pl.contributions': self.participant.vars['player_total_contrib'],
            'bonus_quiz': self.participant.vars['quiz_bonus'],
            'bonus_game': self.player_game_bonus,
        }

        total_payoff = self.tokens_to_dollars(self.quiz_bonus) \
            + self.tokens_to_dollars(self.player_total_withheld) \
            + self.tokens_to_dollars(self.player_game_bonus)

        self.total_payoff = total_payoff
        self.payoff = int(self.player_game_bonus) + int(self.quiz_bonus)
        self.game_result = str(game_result).replace(", ", ",").replace(": ", ":")


    def print_player_game_result_table(self):
        data = {
            "bot_contributions": self.participant.vars["player_bots_contributions"],
            "game_contributions_total": self.participant.vars["player_game_total_contrib"],
            "player_contributions": self.participant.vars["player_contributions"],
            "player_game_bonus" : self.player_game_bonus,
            "player_payoff": self.participant.payoff,
            "player_payoff_plus_partip_fee": self.participant.payoff_plus_participation_fee(),
            "player_quiz_bonus": self.quiz_bonus,
            "player_total_contributed": self.total_contributed,
            "player_total_payoff": self.total_payoff,
            "player_total_withheld": self.player_total_withheld,
            "player_vars": self.participant.vars,
        }

        Functions.print_game_result_table(data)
