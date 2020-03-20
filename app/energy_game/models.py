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
        mock_quiz = "{'correct': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'attempts': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 'bonus': Currency(0)}";
        print('in creating_session', self.round_number)
        for p in self.get_players():
            print(p.participant.vars)
            p.participant.vars['foo'] = 1
            p.participant.vars["quiz_bonus"] = mock_quiz



class Group(BaseGroup):

    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))
    do_once = models.BooleanField(initial=True)
    carbonFund = models.CurrencyField()

    def get_avg_contribution(self):
        print('total_contribution', self.total_contribution)
        return 100 * self.total_contribution / Constants.game_players

    def get_bot_contributions_string(self):
        bot_contributions_str = \
            models.LongStringField(initial=str(self.session.vars["bot_contributions"][0]))

        for i in range(1, len(self.session.vars["bot_contributions"])):
            bot_contributions_str = bot_contributions_str + \
                "\n" + models.LongStringField(initial=str(self.session.vars["bot_contributions"][i]))
        return bot_contributions_str


    def set_bots(self):
        player = self.get_players()[0]
        round_number = self.round_number - 2

        if round_number <= 0:
            contributions = [
                [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4]
            ]

            self.session.vars["bot_contributions"] = contributions
            self.session.vars["cumulative_contributions"] = contributions

        elif round_number == 1:
            contributions = [10, 9, 8, 3, 3, 2, 2, 1, 8, 9, 10, 9, 8, 7, 7, 7, 5, 6, 6, 6, 5, 4, 5, 4]
            self.session.vars["bot_contributions"].append(contributions)

        else:
            player_last_round = player.in_round(self.round_number - 1)
            player_two_rounds_ago = player.in_round(self.round_number - 2)
            player_contribution_last_round = int(player_last_round.contributed)
            player_contribution_two_rounds_ago = int(player_two_rounds_ago.contributed)
            bot_contribution_last_round = self.session.vars["bot_contributions"][-1]
            bot_contribution_two_rounds_ago = self.session.vars["bot_contributions"][-2]

            NUM_RECIPROCATORS = 3
            NUM_FREE_RIDERS = 5
            NUM_CONDITIONALS = 16
            NUM_AGENTS = len(bot_contribution_last_round)
            NUM_CCS_ABOVE = 3
            NUM_CCS_BELOW = 2
            new_contributions = []

            for _ in range(NUM_RECIPROCATORS):
                new_contributions.append(randint(8, 10))

            for _ in range(NUM_FREE_RIDERS):
                new_contributions.append(randint(0, 2))

            is_upward_trend = \
                player_contribution_last_round + sum(bot_contribution_last_round) \
                > player_contribution_two_rounds_ago + sum(bot_contribution_two_rounds_ago)

            mean_last_round = \
                float(player_contribution_last_round \
                + sum(bot_contribution_last_round)) \
                / float(NUM_AGENTS + 1)

            # split agent list into those above mean and those below mean
            cc_indices = list(range(NUM_RECIPROCATORS + NUM_FREE_RIDERS, NUM_AGENTS))

            below_mean = []
            above_mean = []

            for i in cc_indices:
                if bot_contribution_last_round[i] < mean_last_round:
                    below_mean.append(i)
                elif bot_contribution_last_round[i] > mean_last_round:
                    above_mean.append(i)

            # randomly select NUM_CCS_ABOVE and \
            # NUM_CCS_BELOW from the appropriate agents
            shuffle(below_mean)
            shuffle(above_mean)

            modify_above = above_mean[:NUM_CCS_ABOVE:]
            modify_below = below_mean[:NUM_CCS_BELOW:]

            # copy contributions of conditional cooperators
            # and adjust if they're supposed to be adjusted
            for i in cc_indices:
                if i in modify_below and is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] + 1)
                elif i in modify_above and not is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] - 1)
                else:
                    new_contributions.append(bot_contribution_last_round[i])

                # code to make sure no contributions are negative or > 10
                new_contributions[-1] = min(10, max(0, new_contributions[-1]))

            self.session.vars["bot_contributions"].append(new_contributions)

        player.bot_contributions_in_round = str(self.session.vars["bot_contributions"][round_number])


    def set_payoffs(self):
        self.total_contribution = sum([p.contributed for p in self.get_players()])

        for player in self.get_players():
            if self.total_random_contribution:
                self.total_random_contribution = \
                    player.contributed + player.random_others_contribution

            player.payoff = c(10) - player.contributed

            if self.round_number == Const.num_rounds:
                if Const.group_goal <= self.all_rounds_contribution():
                    print("all rounds contributed:")
                    print(self.all_rounds_contribution())
                    print("mulitplier:")
                    print(Const.multiplier)
                    print("players per group:")
                    print(Const.players_per_group)
                    self.bonus = self.all_rounds_contribution() * Const.multiplier / 26
                    player.payoff += self.bonus


    # It's used for after-survey queries.
    def pay_quizzes(self):
        return False
        # if self.do_once and self.round_number == Const.num_rounds:
        #     self.do_once = False
        #     for player in self.get_players():
        #         player.payoff += player.how_many_good_answers()

    def pay_carbonfund(self):
        self.carbonFund = self.all_rounds_contribution()/10*22


    def all_rounds_contribution(self):
        player = self.get_players()[0]
        player_in_all_rounds = player.in_all_rounds()
        player_sum = 0

        for i in range(len(player_in_all_rounds)):
            if player_in_all_rounds[i].contributed != None:
                player_sum += player_in_all_rounds[i].contributed

        group_sum = sum([sum(x) for x in self.session.vars["bot_contributions"]])
        # print(int(player.contributed))
        # player_sum = sum([int(x.contributed) for x in player_in_all_rounds])
        return c(group_sum + player_sum)

    def all_rounds_others_contribution(self):
        return sum([sum(x) for x in self.session.vars["bot_contributions"]])

    def get_total_contribution(self):
        player = self.get_players()[0]
        player_contribution = int(player.contributed)
        group_contributions = sum(self.session.vars["bot_contributions"][self.round_number - 2])
        #     return sum([g.total_contribution for g in self.in_rounds(2, self.round_number)])
        return c(player_contribution + group_contributions)


    def all_rounds_contribution_in_dollars(self):
        return c(self.all_rounds_contribution()).to_real_world_currency(self.session)


    def all_rounds_contribution_donation(self):
        return models.IntegerField(initial=self.all_rounds_contribution())

    def previous_rounds_contribution(self):
        return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)




# Player, group, and subsession objects have the following methods:
# For example, if you are in the last round of a 10-round game,
# player.in_previous_rounds() will return a list with 9 player objects,
# which represent the current participant in all previous rounds.
# - in_previous_rounds()
# - in_all_rounds()
# - in_rounds()
# - in_round()
# -- player.in_all_rounds() is almost the same but the list will have 10 objects, because it includes the current round’s player.
# -- player.in_rounds(m, n) returns a list of players representing the same participant from rounds m to n.
# -- player.in_round(m)
class Player(BasePlayer):
    payoff = 0
    contributed = models.CurrencyField(min=0, max=10)
    withheld = models.CurrencyField(min=0, max=10)

    random_others_contribution = models.CurrencyField()
    bot_contributions_in_round = models.LongStringField()

    participant_vars_dump = models.LongStringField()
    group_random_total_contribution = models.CurrencyField()

    def all_tokens_left(self):
        return c(120) - self.all_rounds_contribution()

    def previous_tokens_left(self):
        return c(120) - self.previous_rounds_contribution()

    def all_rounds_contribution(self):
        return sum([p.contributed for p in self.in_rounds(2, self.round_number)])

    # def all_rounds_practice_contribution(self):
    #     return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_withheld(self):
        return sum([p.practice_withheld for p in self.in_rounds(1, self.round_number)])

    def all_rounds_withheld(self):
        # for p in self.in_rounds(1, self.round_number):
        #     print('round_number', self.round_number)
        #     print('p', Utils.dump_obj(p))
        return sum([p.withheld for p in self.in_rounds(2, self.round_number)])



    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

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


    def others_contribution_array(self):
        return self.session.vars["bot_contributions"][self.round_number-1]

    def all_rounds_others_contributions_array(self):
        return self.session.vars["bot_contributions"]

    # get sum of bot contributions across all rounds
    def all_rounds_others_contribution(self):
        return c(sum([sum(x) for x in self.session.vars["bot_contributions"]]))

    # def others_contribution(self):
    #     return sum([p.contributed for p in self.get_others_in_group()])

    # def others_contribution_array(self):
    #     return [p.contributed for p in self.get_others_in_group()]

    # def all_rounds_others_contribution(self):
    #     return sum([p.all_rounds_contribution() for p in self.get_others_in_group()])

    # def all_rounds_others_contribution_array(self):
    #     return ([p.all_rounds_contribution() for p in self.get_others_in_group()])

    def remaining_tokens_in_dollars(self):
        return c(self.all_tokens_left()).to_real_world_currency(self.session)

    def total_tokens_in_dollars(self):
        return self.remaining_tokens_in_dollars() + self.group.bonus_in_dollars()

    def total_contribution(self):
        if self.round_number <= Const.num_rounds / 2:
            return sum([p.contributed for p in self.in_rounds(1, self.round_number - 1)])
        return sum([p.contributed for p in self.in_rounds(Const.num_rounds / 2 + 1, self.round_number - 1)])

    def total_pay(self):
        return self.group.bonus_in_dollars() \
            + self.remaining_tokens_in_dollars() \
            + c(5).to_real_world_currency(self.session) \
            + c(self.how_many_good_answers()).to_real_world_currency(self.session)



    def how_many_good_answers(self):
        counter = 0
        # answers = [
        #     self.in_round(2).q1 == Const.answers[0],
        #     self.in_round(2).q2 == Const.answers[1],
        #     self.in_round(2).is_both_Examples_right(),
        #     self.in_round(2).is_all_values_right(),
        # ]
        # for answer_is_correct in answers:
        #     if answer_is_correct:
        #         counter += 5
        # return c(counter)
        # self.participant.vars["quiz_bonus"]
        return 0


    # bot_contributions = [
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3],
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3]
    # ]

    # bot_contributions[round number][player number]

    # bot_total_contributions = [
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3],
    #     [20, 18, 16, 6, 6, 4, 4, 2, 16, 20, 20, 18, 16, 16, 14, 14, 12, 12, 12, 10, 10, 8, 8, 8, 6]
    # ]
