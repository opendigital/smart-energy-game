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

# self.player.participant_vars_dump = str(self.participant.vars)

class Subsession(BaseSubsession):

    def creating_session(self):
        self.session.vars["bot_contributions"] = []
        self.session.vars["round_contributions"] = []
        self.session.vars["round_sums"] = []
        self.session.vars["round_withholdings"] = []
        self.session.vars["total_withheld"] = 0
        self.session.vars["round_total"] = 0
        self.session.vars["group_total"] = 0
        self.session.vars["game_total"] = 0

        print("SESSION:", self.session.vars)
        for p in self.get_players():
            print("PARTICIPANT:", p.participant.vars)
            p.participant.vars['contributions'] =[]
            p.participant.vars['witholdings'] =[]
            p.participant.vars['total_witheld'] = 0
            p.participant.vars['total_contributed'] = 0
            p.participant.vars["quiz_bonus"] = 0
            if 'quiz_data' in p.participant.vars:
                quiz_data = p.participant.vars
                p.participant.vars["quiz_bonus"] = quiz_data["quiz_bonus"]



class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()

    group_round_total = models.IntegerField()
    group_round_avg = models.FloatField()

    bot_round_total = models.FloatField()
    bot_round_avg = models.FloatField()

    bot_contributions = models.LongStringField()

    do_once = models.BooleanField(initial=True)
    bonus = models.CurrencyField(initial=c(0))
    carbonfund_total = models.IntegerField()

    def sync_round(self, vars):
        contributions = []
        self.session.vars["group_total"] = self.total_contribution
        self.session.vars["game_total"] = self.total_contribution + self.session.vars["group_total"]

    def get_bot_contributions_string(self):
        bot_contributions_str = models.LongStringField(initial=str(self.session.vars["bot_contributions"][0]))

        for i in range(1, len(self.session.vars["bot_contributions"])):
            bot_contributions_str = bot_contributions_str + \
                "\n" + models.LongStringField(initial=str(self.session.vars["bot_contributions"][i]))
        return bot_contributions_sztr

    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_carbonfund_total(self, value):
        self.carbonfund_total = value

    def set_bot_round_avg(self, value):
        self.bot_round_avg  = value

    def set_group_round_avg(self, value):
        self.group_round_avg = value

    def get_bot_round_avg(self):
        # return float(sum(self.session.vars["round_contributions"]) / Constants.game_players -1)
        return self.group_round_avg

    def print_round_bot_contributions(self):
        print(
            "\n--------------BOT STATS------------------------",
            "\nBots: ", self.bot_contributions,
            "\nSum:  ", self.bot_round_total,
            "\nAvg:  ", self.bot_round_avg,
        )




    def contribution_trend_isupward(self):
        player = self.get_players()[0]
        player_in_round1 = player.in_round(self.round_number - 1).contributed
        player_in_round2 = player.in_round(self.round_number - 2).contributed
        bot_contribution_last = self.session.vars["bot_contributions"][-1]
        bot_contribution_last2 = self.session.vars["bot_contributions"][-2]

        round_sum1 = player_in_round1 + sum(bot_contribution_last)
        round_sum2 = player_in_round2 + sum(bot_contribution_last2)
        return round_sum1 > round_sum2


    def set_bots(self):
        player = self.get_players()[0]
        round_number = self.round_number
        print("\n\n\nROUND NUMBER", round_number)
        NUM_AGENTS = Constants.game_players -1
        NUM_RECIPROCATORS = 3
        NUM_FREE_RIDERS = 5
        NUM_CONDITIONALS = 16
        NUM_CCS_ABOVE = 3
        NUM_CCS_BELOW = 2
        new_contributions = []

        round_index = self.round_number - 2

        if round_index <= 0:
            new_contributions = [10,9,8,3,3,2,2,1,8,10,10,9,8,8,7,7,6,6,6,5,5,4,4,4]
        elif round_index == 1:
            new_contributions = [10,9,8,3,3,2,2,1,8, 9,10,9,8,7,7,7,5,6,6,6,5,4,5,4]
        else:
            bot_contributions = self.session.vars["bot_contributions"]

            player_last_round = player.in_round(self.round_number-1)
            player_contribution_last_round = int(player_last_round.contributed)
            bot_contribution_last_round = self.session.vars["bot_contributions"][-1]

            player_two_rounds_ago = player.in_round(self.round_number-2)
            player_contribution_two_rounds_ago = int(player_two_rounds_ago.contributed)


            # cooperator contributions
            for _ in range(NUM_RECIPROCATORS):
                new_contributions.append(randint(8, 10))
            # free rider contributions
            for _ in range(NUM_FREE_RIDERS):
                new_contributions.append(randint(0, 2))

            is_upward_trend = self.contribution_trend_isupward()
            mean_last_round = float(player_contribution_last_round + sum(bot_contribution_last_round)) / float(NUM_AGENTS + 1)

            # split agent list into those above mean and those below mean
            cc_indices = list(range(NUM_RECIPROCATORS + NUM_FREE_RIDERS, NUM_AGENTS))
            below_mean = []
            above_mean = []

            # randomly select NUM_CCS_ABOVE and NUM_CCS_BELOW from the appropriate agents
            for i in cc_indices:
                if bot_contribution_last_round[i] < mean_last_round:
                    below_mean.append(i)
                elif bot_contribution_last_round[i] > mean_last_round:
                    above_mean.append(i)

            shuffle(below_mean)
            shuffle(above_mean)
            modify_above = above_mean[:NUM_CCS_ABOVE:]
            modify_below = below_mean[:NUM_CCS_BELOW:]

            print(bot_contribution_last_round)
            # copy contributions of conditional cooperators and adjust if they're supposed to be
            for i in cc_indices:
                if i in modify_below and is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] + 1)
                elif i in modify_above and not is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] - 1)
                else:
                    new_contributions.append(bot_contribution_last_round[i])
                new_contributions[-1] = min(10, max(0, new_contributions[-1]))
            print("\tPREV_AVG\t", mean_last_round)

        self.session.vars["round_contributions"] = new_contributions
        self.session.vars["bot_contributions"].append(new_contributions)
        self.bot_contributions = str(new_contributions)
        self.bot_round_total = sum(new_contributions)
        self.bot_round_avg = float(self.bot_round_total / len(new_contributions))
        print("\tCURR_AVG\t", self.bot_round_avg)



    def set_payoffs(self):
        for player in self.get_players():
            player_contributed = player.contributed
            player_witheld = player.withheld
            player_total_contributed = sum(player.participant.vars["contributions"]) + player_contributed
            player_total_witheld = sum(player.participant.vars["witholdings"]) + player_witheld

            player.participant.vars['contributions'].append(player_contributed)
            player.participant.vars['witholdings'].append(player_witheld)
            player.participant.vars["total_contributed"] = player_total_contributed
            player.participant.vars["total_witheld"] = player_total_witheld
            player.payoff = player_witheld

            if self.round_number == Const.num_rounds:
                if Const.group_goal <= self.all_rounds_contribution():
                    self.bonus = self.all_rounds_contribution() * Const.multiplier / 26
                    player.payoff += self.bonus


    def set_total_contribution(self):
        game_fixed_sum = Constants.game_players * 10
        player = self.get_players()[0]
        bot_round_total = sum(self.session.vars["round_contributions"])
        group_round_total = bot_round_total + player.contributed
        round_witholdings = game_fixed_sum - group_round_total

        self.group_round_total = group_round_total
        self.group_round_avg = group_round_total / Constants.game_players

        self.session.vars["group_total"] = bot_round_total
        self.session.vars['round_total'] = group_round_total
        self.session.vars["round_withholdings"].append(round_witholdings)
        self.session.vars['round_sums'].append(group_round_total)

        game_withheld = self.session.vars["total_withheld"]
        game_total = self.session.vars["game_total"]

        self.session.vars["total_withheld"] = game_withheld + round_witholdings
        self.session.vars["game_total"] = game_total + group_round_total


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

    def bonus_in_quiz_datas(self):
        return self.bonus.to_real_world_currency(self.session)

    def finalize_game_data(self):
        print('done')



class Player(BasePlayer):
    contributed = models.IntegerField(min=0, max=10)
    withheld = models.IntegerField(min=0, max=10)
    contributions = models.LongStringField()
    quiz_bonus = models.IntegerField()

    def update_player_round(self):
        print("player", "sync_player_round", self.participant)

    def compute_payouts(self):
        game_total = self.session.vars["game_total"]
        quiz_bonus = self.participant.vars["quiz_bonus"]
        player_withheld = self.participant.vars["total_witheld"]
        if game_total >= Constants.group_goal:
            game_bonus = game_total
        else:
            game_bonus = 0;
        carbonfund_total = game_total + game_bonus
        participation_pay_usd = Constants.participation_pay



    def init_player(self):
        return
        if 'quiz_data' in self.participant.vars:
            print("player", "quiz_data", self.participant.vars["quiz_data"])

    def print_round_results(self, data):
        return
        print('=========================================================')
        print('ROUND NUMBER', self.round_number)
        print('game_total                   \t', data["game_total"])
        print('=========================================================')
        print('player_withheld              \t', data["player_withheld"])
        print('player_contributed           \t', data["player_contributed"])
        print('--------------------------------------------------------')
        print('player_total_witheld         \t', data["player_total_witheld"])
        print('player_total_contributed     \t', data["player_total_contributed"])
        print('--------------------------------------------------------')
        print('group_round_contributions    \t', data["group_round_contributions"])
        print('group_round_withholdings     \t', data["group_round_withholdings"])
        print('--------------------------------------------------------')
        print('group_total_withheld         \t', data["group_total_withheld"])
        print('group_round_total            \t', data["group_round_total"])
        print('player_past_contributions    \t', data["player_past_contributions"])
        print('player_past_witholdings      \t', data["player_past_witholdings"])
        print('group_round_sums        \t',      data["round_sums"])
        print('\n\n')

    def finalize_game_data(self):
        self.participant.vars["game_result"] = str(self.participant.vars)
        print(str(self.participant.vars))
        print('=======================FINAL=============================')
        print('game_total                   \t', self.session.vars["game_total"])
        print('=========================================================')
        print('total_contributed           \t', self.participant.vars["total_contributed"])
        print('total_witheld               \t', self.participant.vars["total_witheld"])
        print('quiz_bonus               \t', self.participant.vars["quiz_bonus"])
        # print(self.session.vars["bot_contributions"])
