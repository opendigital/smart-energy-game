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
        print('in creating_session', self.round_number)
        self.session.vars["bot_contributions"] = []
        self.session.vars["round_contributions"] = []
        self.session.vars["round_sums"] = []
        self.session.vars["round_withholdings"] = []
        self.session.vars["total_withheld"] = 0
        self.session.vars["round_total"] = 0
        self.session.vars["group_total"] = 0
        self.session.vars["game_total"] = 0

        print(self)
        for p in self.get_players():
            print(p.participant)
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
    bot_contributions = models.LongStringField()
    do_once = models.BooleanField(initial=True)
    bonus = models.CurrencyField(initial=c(0))
    carbonfund_total = models.IntegerField()

    def sync_round(self, vars):
        contributions = []
        self.session.vars["group_total"] = self.total_contribution
        self.session.vars["game_total"] = self.total_contribution + self.session.vars["group_total"]

    def get_bot_contributions_string(self):
        bot_contributions_str = \
            models.LongStringField(initial=str(self.session.vars["bot_contributions"][0]))

        for i in range(1, len(self.session.vars["bot_contributions"])):
            bot_contributions_str = bot_contributions_str + \
                "\n" + models.LongStringField(initial=str(self.session.vars["bot_contributions"][i]))
        return bot_contributions_sztr

    def tokens_to_dollars(self, value):
        return c(value).to_real_world_currency(self.session)

    def set_carbonfund_total(self, value):
        self.carbonfund_total = value


    def set_bots(self):
        player = self.get_players()[0]
        round_number = self.round_number
        NUM_AGENTS = Constants.game_players -1
        NUM_RECIPROCATORS = 3
        NUM_FREE_RIDERS = 5
        NUM_CONDITIONALS = 16
        NUM_CCS_ABOVE = 3
        NUM_CCS_BELOW = 2
        new_contributions = []

        if round_number <= 1:
            new_contributions = [10,9,8,3,3,2,2,1,8,10,10,9,8,8,7,7,6,6,6,5,5,4,4,4]
            self.session.vars["round_contributions"] = new_contributions
            self.session.vars["bot_contributions"].append(new_contributions)
        elif round_number == 2:
            new_contributions = [10, 9, 8, 3, 3, 2, 2, 1, 8, 9, 10, 9, 8, 7, 7, 7, 5, 6, 6, 6, 5, 4, 5, 4]
            self.session.vars["bot_contributions"].append(new_contributions)
            self.session.vars["round_contributions"] = new_contributions
        else:
            player_last_round = player.in_round(self.round_number - 1)
            player_contribution_last_round = int(player_last_round.contributed)
            bot_contribution_last_round = self.session.vars["bot_contributions"][-1]

            player_two_rounds_ago = player.in_round(self.round_number - 2)
            player_contribution_two_rounds_ago = int(player_two_rounds_ago.contributed)
            bot_contribution_two_rounds_ago = self.session.vars["bot_contributions"][-2]

            for _ in range(NUM_RECIPROCATORS):
                new_contributions.append(randint(8, 10))
            for _ in range(NUM_FREE_RIDERS):
                new_contributions.append(randint(0, 2))

            is_upward_trend = player_contribution_last_round + sum(bot_contribution_last_round) > player_contribution_two_rounds_ago \
                + sum(bot_contribution_two_rounds_ago)

            mean_last_round = float(player_contribution_last_round + sum(bot_contribution_last_round)) / float(NUM_AGENTS + 1)

            cc_indices = list(range(NUM_RECIPROCATORS + NUM_FREE_RIDERS, NUM_AGENTS))
            below_mean = []
            above_mean = []

            for i in cc_indices:
                if bot_contribution_last_round[i] < mean_last_round:
                    below_mean.append(i)
                elif bot_contribution_last_round[i] > mean_last_round:
                    above_mean.append(i)

            shuffle(below_mean)
            shuffle(above_mean)

            modify_above = above_mean[:NUM_CCS_ABOVE:]
            modify_below = below_mean[:NUM_CCS_BELOW:]

            for i in cc_indices:
                if i in modify_below and is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] + 1)
                elif i in modify_above and not is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] - 1)
                else:
                    new_contributions.append(bot_contribution_last_round[i])
                new_contributions[-1] = min(10, max(0, new_contributions[-1]))

            # print('prev round 0', new_contributions)
            # print('prev round 1', self.session.vars["bot_contributions"][-1])
            # print('prev round 2', self.session.vars["bot_contributions"][-2])
            self.session.vars["round_contributions"] = new_contributions
            self.session.vars["bot_contributions"].append(new_contributions)
        self.bot_contributions = str(new_contributions)


    def set_payoffs(self):
        print("group", "set_payoffs")
        print(self.session.vars)
        for player in self.get_players():

            print(player.participant.vars)
            player_contributed = player.contributed
            player_witheld = player.withheld

            player_total_contributed = sum(player.participant.vars["contributions"]) + player_contributed
            player_total_witheld = sum(player.participant.vars["witholdings"]) + player_witheld

            player.participant.vars['contributions'].append(player_contributed)
            player.participant.vars['witholdings'].append(player_witheld)
            player.participant.vars["total_contributed"] = player_total_contributed
            player.participant.vars["total_witheld"] = player_total_witheld

            # if self.total_random_contribution: self.total_random_contribution = player_contributed + player.random_others_contribution

            player.payoff = 10 - player_witheld
            if self.round_number == Const.num_rounds:
                if Const.group_goal <= self.all_rounds_contribution():
                    self.bonus = self.all_rounds_contribution() * Const.multiplier / 26
                    player.payoff += self.bonus
        print("group", "set_payoffs", "player_contributed", player_contributed)



    def set_total_contribution(self):
        game_fixed_sum = Constants.game_players * 10
        player = self.get_players()[0]
        bot_round_total = sum(self.session.vars["round_contributions"])
        player_group_sum = bot_round_total + player.contributed
        self.session.vars["group_total"] = bot_round_total
        round_witholdings = game_fixed_sum - player_group_sum
        self.session.vars["round_withholdings"].append(round_witholdings)
        self.session.vars['round_sums'].append(player_group_sum)
        self.session.vars['round_total'] = player_group_sum
        game_withheld = self.session.vars["total_withheld"]
        game_total = self.session.vars["game_total"]

        self.session.vars["total_withheld"] = game_withheld + round_witholdings
        self.session.vars["game_total"] = game_total + player_group_sum
        return self.session.vars["game_total"]



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

    def sync_player_round(self):
        print("player", "sync_player_round", self.participant)
        # if self.participant.vars:


    def init_player(self):
        print("player", "init_player", self)
        if self.round == 0:
            print("how")

        if self.round == 1:
            print("now")

        if 'quiz_data' in self.participant.vars:
            print("player", "quiz_data", self.participant.vars["quiz_data"])

        # self.payoff = if self.
        # self.contributions = self.p
            # print(p.participant)


    def all_rounds_withheld(self):
        # for p in self.in_rounds(1, self.round_number):
        #     print('round_number', self.round_number)
        #     print('p', Utils.dump_obj(p))
        return sum([p.withheld for p in self.in_rounds(2, self.round_number)])



    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    # def all_rounds_group_random_contribution(self):
    #     return sum([p.group_random_total_contribution \
    #     for p in self.in_rounds(1, self.round_number)])

    def previous_rounds_contribution(self):
        if self.round_number <= Const.num_rounds / 2:
            return sum([
                p.contributed for p in self.in_rounds(
                    1,
                    self.round_number - 1
                )
            ])
        return sum([
            p.contributed for p in self.in_rounds(
                Const.num_rounds / 2 + 1,
                self.round_number - 1
            )
        ])


    def others_contribution(self):
        return c(sum(self.session.vars["bot_contributions"][self.round_number-1]))

    def remaining_tokens_in_quiz_datas(self):
        return c(self.all_tokens_left()).to_real_world_currency(self.session)


    def total_tokens_in_quiz_datas(self):
        return self.remaining_tokens_in_quiz_datas() + self.group.bonus_in_quiz_datas()


    def finalize_game_payout(self):
        usd2points = self.session["real_world_currency_per_point"]  #0.01,
        participation_fee = self.session["participation_fee"]  #0.50,
        self.participant.vars["quiz_bonus"]
        bonus_multipler=1
        if Constants.group_goal <= self.session.vars["game_total"]:
            bonus_multipler=2


    def finalize_game_player_data(self):
        self.participant.vars["game_result"] = str(self.participant.vars)
        print(str(self.participant.vars))
