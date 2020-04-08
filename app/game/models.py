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

Const = Constants
AUTHOR = 'Matt Harris <m@harr.is>'

DOC = """
RCODI Energy Game - Main App
"""



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

    def finalize_group_round_data(self):
        self.set_bot_contributions()
        self.finalize_group_player_data()
        self.set_group_aggregate_data()

    def finalize_group_game_data(self):
        self.game_total_contrib = self.session.vars["game_total_contrib"]
        if self.game_total_contrib >= Constants.group_goal:
            self.group_game_bonus = self.game_total_contrib
        else:
            self.group_game_bonus = 0;

        self.set_carbonfund_total()

        for player in self.get_players():
            player.set_player_round_name()
            player.finalize_game_player_data()
            player.cleanup_session_variables()

            if Constants.print_game_result_table:
                player.print_game_result_table()

    def get_bot_contributions_string(self):
        bot_contributions_str = models.LongStringField(initial=str(self.session.vars["bot_contributions"][0]))
        for i in range(1, len(self.session.vars["bot_contributions"])):
            bot_contributions_str = bot_contributions_str + \
                "\n" + models.LongStringField(initial=str(self.session.vars["bot_contributions"][i]))
        return bot_contributions_str

    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_carbonfund_total(self):
        self.carbonfund_total = self.game_total_contrib

    def set_bot_round_avg(self, value):
        self.bot_round_avg  = value

    def set_group_round_avg(self, value):
        self.group_round_avg = value

    def get_bot_round_avg(self):
        return self.group_round_avg

    def print_bot_round_result(self, round, diff, trend):
        round_str=''
        diff_str=''
        for val in round:
            round_str += str(val).rjust(4, ' ')
        round_str += "|count: " + str(len(round))
        round_str += "|sum: " + str(sum(round))
        round_str += "|avg: " + str(float(sum(round) / len(round)))
        round_str += "|trend: " + trend
        print(round_str)
        for val in diff:
            diff_str += str(val).rjust(4, ' ')
        print(diff_str)


    def get_contribution_trend(self):
        player = self.get_players()[0]
        player_round_n1 = player.in_round(self.round_number - 1).contributed
        player_round_n2 = player.in_round(self.round_number - 2).contributed
        bot_contribution_last = self.session.vars["bot_contributions"][-1]
        bot_contribution_last2 = self.session.vars["bot_contributions"][-2]
        group_contribution_total1 = player_round_n1 + sum(bot_contribution_last)
        group_contribution_total2 = player_round_n2 + sum(bot_contribution_last2)

        if group_contribution_total1 > group_contribution_total2:
            return "up"
        elif group_contribution_total1 < group_contribution_total2:
            return "down"
        else:
            return "stable"

    def set_contribution_range(self, minval, maxval, value):
        return min(maxval, max(minval, value))


    def set_bot_contributions(self):
        player = self.get_players()[0]
        round_number = self.round_number
        NUM_AGENTS = Constants.game_players -1
        NUM_COOPERATORS = 3
        NUM_FREE_RIDERS = 5
        NUM_RECIPROCATORS = 16
        NUM_RECIPROCATORS_ABOVE = 3
        NUM_RECIPROCATORS_BELOW = 2

        cooperator_list = [10,9,8]
        freerider_list = [3,3,2,2,1]
        if self.round_number <= 1:
            reciprocator_list = [8,10,10,9,8,8,7,7,6,6,6,5,5,4,4,4]
        elif self.round_number == 2:
            reciprocator_list = [8, 9,10,9,8,7,7,7,5,6,6,6,5,4,5,4]
        else:
            bots_round_n1_contributions = self.session.vars["bot_contributions"][-1]
            player_round_n1 = player.in_round(self.round_number-1)
            player_round_n1_contributed = int(player_round_n1.contributed)
            round_n1_sum = player_round_n1_contributed + sum(bots_round_n1_contributions)
            round_n1_avg = float(round_n1_sum / (len(bots_round_n1_contributions) + 1))

            trend = self.get_contribution_trend()
            prev_reciprocators = bots_round_n1_contributions[:NUM_RECIPROCATORS:]

            rcp_below_avg=[]
            rcp_above_avg=[]

            for item in prev_reciprocators:
                if item < round_n1_avg:
                    rcp_below_avg.append(item)
                elif item >= round_n1_avg:
                    rcp_above_avg.append(item)
                else:
                    rcp_above_avg.append(item)

            shuffle(rcp_below_avg)
            shuffle(rcp_above_avg)
            reciprocator_changelist = rcp_below_avg[:NUM_RECIPROCATORS_BELOW] + rcp_above_avg[-NUM_RECIPROCATORS_ABOVE:]
            diff = []
            new_set=[]
            for value in prev_reciprocators:
                delta=" "
                # ----------------------
                # RECIPROCITY NORM RULES: Trend is up/down
                # SOCIAL NORM RULES: value vs group avg
                # ----------------------
                if value in reciprocator_changelist:
                    delta="."
                    reciprocator_changelist.remove(value)
                    if trend == "up" and value <= round_n1_avg:
                        value = self.set_contribution_range(0, 10, value + 1)
                        delta = "+"
                    elif trend == "stable" and value <= round_n1_avg:
                        value = self.set_contribution_range(0, 10, value + 1)
                        delta = "+"
                    elif trend == "down" and value > round_n1_avg:
                        value = self.set_contribution_range(0, 10, value - 1)
                        delta = "-"
                new_set.append(value)
                diff.append(delta)

            reciprocator_list = new_set

        new_contributions = reciprocator_list + cooperator_list + freerider_list
        self.session.vars["bot_round_contributions"] = new_contributions
        self.session.vars["bot_contributions"].append(new_contributions)
        self.bot_contributions = str(new_contributions).replace(" ", "")
        self.bot_round_contrib_total = sum(new_contributions)
        self.bot_round_avg = float(self.bot_round_contrib_total / len(new_contributions))


    def finalize_group_player_data(self):
        for player in self.get_players():
            player.set_player_round_data()

    def set_group_aggregate_data(self):
        round_fixed_sum = Constants.game_players * 10
        player_round_contrib = self.session.vars["player_round_contrib"]
        player_round_withheld = 10 - player_round_contrib

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
            if player_in_all_rounds[i].contributed != None:
                player_sum += player_in_all_rounds[i].contributed

        group_sum = sum([sum(x) for x in self.session.vars["bot_contributions"]])
        return c(group_sum + player_sum)

    def all_rounds_contribution_donation(self):
        return models.IntegerField(initial=self.all_rounds_contribution())


class Player(BasePlayer):
    round = models.StringField()
    contributed = models.IntegerField(min=0, max=10)
    withheld = models.IntegerField(min=0, max=10)
    total_contributed = models.IntegerField()
    total_witheld = models.IntegerField()
    contributions = models.LongStringField()
    # participation_pay = models.IntegerField()
    player_game_bonus = models.FloatField()
    quiz_bonus = models.IntegerField()
    total_payoff = models.CurrencyField()
    game_result = models.LongStringField()

    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_player_round_name(self):
        if self.round_number == Constants.num_rounds:
            round_title = "rZ"
        else:
            round_title = "r" + str(self.round_number)
        self.round = round_title


    def set_player_round_data(self):
        self.set_player_round_name()
        self.session.vars['player_round_contrib'] = self.contributed

        player_total_contrib = sum(self.participant.vars["player_contributions"]) + self.contributed
        player_total_witheld = sum(self.participant.vars["player_witholdings"]) + self.withheld

        self.participant.vars["player_total_contrib"] = player_total_contrib
        self.participant.vars["player_total_witheld"] = player_total_witheld
        self.participant.vars['player_contributions'].append(self.contributed)
        self.participant.vars['player_witholdings'].append(self.withheld)

        self.payoff = self.withheld


    def init_player(self):
        # self.participation_pay = Constants.participation_pay
        if 'quiz_data' in self.participant.vars:
            self.quiz_bonus = self.participant.vars["quiz_bonus"]
        else:
            self.quiz_bonus = 0

    # def record_bot_round_contributions(self):
    #     bot_contributions = [[10 for x in round_] for round_ in self.bot_contributions]
    #     print('bot_contributions', self.bot_contributions)
    #     self.bot_contributions = bot_contributions


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


    def print_round_results(self, data):
        return
        print('=========================================================')
        print('ROUND NUMBER', self.round_number)
        print('game_total_contrib                   \t', data["game_total_contrib"])
        print('=========================================================')
        print('player_withheld              \t', data["player_withheld"])
        print('player_contributed           \t', data["player_contributed"])
        print('--------------------------------------------------------')
        print('player_total_witheld         \t', data["player_total_witheld"])
        print('player_total_contrib     \t', data["player_total_contrib"])
        print('--------------------------------------------------------')
        print('group_round_contributions    \t', data["group_round_contributions"])
        print('group_round_withholdings     \t', data["group_round_withholdings"])
        print('--------------------------------------------------------')
        print('group_round_contrib_total         \t', data["group_round_contrib_total"])
        print('group_round_witheld_total         \t', data["group_round_witheld_total"])
        print('player_past_contributions    \t', data["player_past_contributions"])
        print('player_past_witholdings      \t', data["player_past_witholdings"])
        print('group_round_contrib        \t',      data["group_round_contrib"])
        print('\n\n')



    def print_game_result_table(self):
        # print(str(self.session.vars).replace("],", "],\n ").replace("[[", "[\n["))
        print('=================================================================================================================')
        print('    #  |  P  | BOTS                                                                    |  t   Δt   x̄    Δx̄       ')
        print('-----------------------------------------------------------------------------------------------------------------')

        player_contributions = self.participant.vars["player_contributions"].copy()
        bot_contributions = self.session.vars["bot_contributions"]
        game_total_contrib = 0
        round_num = 0

        for bot_round in bot_contributions:
            round_num += 1
            player_round = (player_contributions.pop(0))
            player_round_str = "[ " + str(player_round).rjust(2, ' ')

            if round_num > 1:
                round_total_prev = bot_round_total
                bot_round_total = sum(bot_round) + int(player_round)
                diff_total = int(bot_round_total) - int(round_total_prev)

                if (diff_total > 0):
                    diff_total_str = "(+" + str(diff_total) + ")"
                elif (diff_total < 0):
                    diff_total_str = "(" + str(diff_total)+ ")"
                else:
                    diff_total_str = ""
            else:
                bot_round_total = sum(bot_round) + int(player_round)
                diff_total_str = ""


            if round_num > 1:
                round_avg_prev = round_avg
                round_avg = float(bot_round_total / (len(bot_round) + 1))
                diff_avg = round(float(round_avg) - float(round_avg_prev), 4)

                if (diff_avg > 0):
                    diff_avg_str = "(+" + str(diff_avg).ljust(4, '0') + ")"
                elif (diff_avg < 0):
                    diff_avg_str = "(" + str(diff_avg).ljust(4, '0')+ ")"
                else:
                    diff_avg_str = "    "
            else:
                diff_avg_str = "    "
                round_avg = float(bot_round_total / (len(bot_round) + 1))

            round_avg_str = str(round_avg).ljust(4, '0')
            game_total_contrib += bot_round_total
            bot_round_str = ""
            for bot_val in bot_round:
                bot_round_str += str(bot_val).rjust(3, ' ')

            print(
                "|| ("+ str(round_num) + ")",
                player_round_str, "|",
                bot_round_str.lstrip(), "]", '|',
                str(bot_round_total),
                str(diff_total_str).rjust(4, ' '),
                str(round_avg_str),
                str(diff_avg_str).rjust(7, ' '), '||',
                str(game_total_contrib)
            )

        print('-----------------------------------------------------------------------------------------------------------------')
        print('GAME TOTAL:                \t', self.session.vars["game_total_contrib"])
        print('_________________________________________________________')
        print('PLAYER:')
        print('  player_contributions       \t', self.participant.vars["player_total_contrib"], self.contributions)
        print('  total contrib              \t', self.participant.vars["player_total_contrib"], self.total_contributed)
        print('  total witheld              \t', self.participant.vars["player_total_witheld"], self.total_witheld)
        # print('  participation_pay          \t', self.participation_pay)
        print('  total_payoff               \t', self.total_payoff)
        print('  quiz_bonus                 \t', self.quiz_bonus)
        print('  game_bonus                 \t', self.player_game_bonus)
        print('  payoff                     \t', self.payoff)
        print('  self.participant.payoff    \t', self.participant.payoff)
        print('  payoff_plus_partip_fee     \t', self.participant.payoff_plus_participation_fee())

        print('\n\n')
        print(self.participant.vars)
