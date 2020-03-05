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
from .constants import Constants

Const = Constants

author = 'Juan Camilo Cardenas Gomez'
doc = """
Solution for training problem
"""

def get_int_field(_label='', _min=0, _max=9999, _initial=None):
    """Return otree text field type"""
    return models.IntegerField(
        label=_label,
        min=_min,
        max=_max,
        initial=_initial,
    )

def get_text_field(_label=''):
    """Return otree integer field type"""
    return models.StringField(label=_label)

def get_range_field(_label, _choices):
    """Return otree select field type"""
    return models.IntegerField(
        label=_label,
        choices=_choices,
    )

def get_select_field(_label, _choices):
    """Return otree select field type"""
    return models.StringField(
        label=_label,
        choices=_choices,
    )

def get_radiorange_field(_label, _choices, _horiz=False):
    """Return otree select field type"""
    if _horiz:
        _widget = widgets.RadioSelectHorizontal
    else:
        _widget = widgets.RadioSelect

    return models.IntegerField(
        label=_label,
        choices=_choices,
        widget=_widget
    )

def get_yesno_field(_label):
    """Return otree true/false field type"""
    return models.BooleanField(
        label=_label,
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ]
    )

def get_truefalse_field(_label, _choices):
    """Return otree true/false field type"""
    return models.BooleanField(
        label=_label,
        choices=[True, False]
    )

def get_likert_field(_label, _choices):
    """Return otree likert scale field type"""
    return models.IntegerField(
        label=_label,
        widget=widgets.RadioSelect,
        choices=_choices
    )


class Subsession(BaseSubsession):
    """model docstring"""
    pass


class Group(BaseGroup):
    """model docstring"""
    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))
    do_once = models.BooleanField(initial=True)
    carbonFund = models.CurrencyField()

    def get_bot_contributions_string(self):
        bot_contributions_str = models.LongStringField(initial=str(self.session.vars["bot_contributions"][0]))
        for i in range(1, len(self.session.vars["bot_contributions"])):
            bot_contributions_str = bot_contributions_str + \
                "\n" + \
                models.LongStringField(initial=str(self.session.vars["bot_contributions"][i]))

        return bot_contributions_str

    def set_bots(self):
        player = self.get_players()[0]
        round_number = self.round_number - 2

        if round_number <= 0:
            # set initial condition for round 0
            contributions = [
                [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4]
            ]

            # initialize cumulative contributions
            self.session.vars["bot_contributions"] = contributions
            self.session.vars["cumulative_contributions"] = contributions
        elif round_number == 1:
            # set initial condition for round 1
            contributions = [10, 9, 8, 3, 3, 2, 2, 1, 8, 9, 10, 9, 8, 7, 7, 7, 5, 6, 6, 6, 5, 4, 5, 4]
            self.session.vars["bot_contributions"].append(contributions)
        else:
            # get key data on prior rounds
            player_last_round = player.in_round(self.round_number - 1)
            player_two_rounds_ago = player.in_round(self.round_number - 2)
            player_contribution_last_round = int(player_last_round.contribution)
            player_contribution_two_rounds_ago = int(player_two_rounds_ago.contribution)
            bot_contribution_last_round = self.session.vars["bot_contributions"][-1]
            bot_contribution_two_rounds_ago = self.session.vars["bot_contributions"][-2]

            # initialize basic constants
            NUM_RECIPROCATORS = 3
            NUM_FREE_RIDERS = 5
            NUM_CONDITIONALS = 16
            NUM_AGENTS = len(bot_contribution_last_round)
            NUM_CCS_ABOVE = 3
            NUM_CCS_BELOW = 2
            new_contributions = []

            # cooperator contributions
            for _ in range(NUM_RECIPROCATORS):
                new_contributions.append(randint(8, 10))

            # free rider contributions
            for _ in range(NUM_FREE_RIDERS):
                new_contributions.append(randint(0, 2))

            # identify factors needed to see if agents should be adjusted
            is_upward_trend = player_contribution_last_round \
                + sum(bot_contribution_last_round) \
                > player_contribution_two_rounds_ago \
                + sum(bot_contribution_two_rounds_ago)

            mean_last_round = float(player_contribution_last_round \
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

            # randomly select NUM_CCS_ABOVE and NUM_CCS_BELOW from the appropriate agents
            shuffle(below_mean)
            shuffle(above_mean)
            modify_above = above_mean[:NUM_CCS_ABOVE:]
            modify_below = below_mean[:NUM_CCS_BELOW:]

            # copy contributions of conditional cooperators and adjust if they're supposed to be
            # adjusted
            for i in cc_indices:
                if i in modify_below and is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] + 1)
                elif i in modify_above and not is_upward_trend:
                    new_contributions.append(bot_contribution_last_round[i] - 1)
                else:
                    new_contributions.append(bot_contribution_last_round[i])

                # code to make sure no contributions are negative or > 10
                new_contributions[-1] = min(10, max(0, new_contributions[-1]))

            # send to the bot contribution array
            self.session.vars["bot_contributions"].append(new_contributions)

        # store bot contributions
        player.bot_contributions_in_round = \
            str(self.session.vars["bot_contributions"][round_number])

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

        for player in self.get_players():
            if self.total_random_contribution:
                self.total_random_contribution = \
                    player.contribution + player.random_others_contribution

            player.payoff = c(10) - player.contribution

            if self.round_number == Const.num_rounds:
                if Const.group_goal <= self.all_rounds_contribution():
                    print("all rounds contribution:")
                    print(self.all_rounds_contribution())
                    print("mulitplier:")
                    print(Const.multiplier)
                    print("players per group:")
                    print(Const.players_per_group)
                    self.bonus = self.all_rounds_contribution() * Const.multiplier / 26
                    player.payoff += self.bonus

    # It's used for after-survey queries.
    def pay_quizzes(self):
        if self.do_once and self.round_number == Const.num_rounds:
            self.do_once = False
            for player in self.get_players():
                player.payoff += player.how_many_good_answers()
        #return

    def pay_carbonfund(self):
        self.carbonFund = self.all_rounds_contribution()/10*22
        #return

    def all_rounds_contribution(self):
        player = self.get_players()[0]
        player_in_all_rounds = player.in_all_rounds()
        player_sum = 0
        for i in range(len(player_in_all_rounds)):
            if player_in_all_rounds[i].contribution != None:
                player_sum += player_in_all_rounds[i].contribution

        group_sum = sum([sum(x) for x in self.session.vars["bot_contributions"]])
        # print(int(player.contribution))

        # player_sum = sum([int(x.contribution) for x in player_in_all_rounds])
        return c(group_sum + player_sum)

    def all_rounds_others_contribution(self):
        return sum([sum(x) for x in self.session.vars["bot_contributions"]])

    def total_contribution(self):
        player = self.get_players()[0]
        player_contribution = int(player.contribution)
        group_contributions = sum(self.session.vars["bot_contributions"][self.round_number - 2])
        return c(player_contribution + group_contributions)

    #     return sum([g.total_contribution for g in self.in_rounds(2, self.round_number)])

    def all_rounds_contribution_in_dollars(self):
        return c(self.all_rounds_contribution()).to_real_world_currency(self.session)

    def all_rounds_contribution_donation(self):
        return models.IntegerField(initial=self.all_rounds_contribution())

    # It's used for before-survey queries.
    def previous_rounds_contribution(self):
        return sum([g.total_contribution for g in self.in_previous_rounds()])

    def bonus_in_dollars(self):
        return self.bonus.to_real_world_currency(self.session)


class Player(BasePlayer):

    def all_tokens_left(self):
        return c(120) - self.all_rounds_contribution()

    def previous_tokens_left(self):
        return c(120) - self.previous_rounds_contribution()

    def all_rounds_contribution(self):
        return sum([p.contribution for p in self.in_rounds(2, self.round_number)])

    def all_rounds_practice_contribution(self):
        return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_private_contribution(self):
        return sum([p.practice_private_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_private_contribution(self):
        return sum([p.private_contribution for p in self.in_rounds(2, self.round_number)])

    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

    def previous_rounds_contribution(self):
        if self.round_number <= Const.num_rounds / 2:
            return sum([
                p.contribution for p in self.in_rounds(
                    1,
                    self.round_number - 1
                )
            ])
        return sum([
            p.contribution for p in self.in_rounds(
                Const.num_rounds / 2 + 1,
                self.round_number - 1
            )
        ])

    def others_contribution(self):
        return c(sum(self.session.vars["bot_contributions"][self.round_number -2]))

    def others_contribution_array(self):
        return self.session.vars["bot_contributions"][self.round_number -2]

    def all_rounds_others_contributions_array(self):
        return self.session.vars["bot_contributions"]

    def all_rounds_others_contribution(self):
        # get sum of bot contributions across all rounds
        return c(sum([sum(x) for x in self.session.vars["bot_contributions"]]))

    # def others_contribution(self):
    #     return sum([p.contribution for p in self.get_others_in_group()])

    # def others_contribution_array(self):
    #     return [p.contribution for p in self.get_others_in_group()]

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
            return sum([p.contribution for p in self.in_rounds(1, self.round_number - 1)])
        return sum([p.contribution for p in self.in_rounds(Const.num_rounds / 2 + 1, self.round_number - 1)])

    def check_answers(self):
        if self.quiz_1 == Const.answers[0] \
                and self.quiz_2 == Const.answers[1] \
                and self.quiz_3a == Const.answers[2] \
                and self.quiz_3b == Const.answers[3]:
            self.everything_correct = True
            return True

        self.everything_correct = False
        return False

    def is_equilibrium_tokens_correct(self):
        if self.quiz_1 == Const.answers[0] and self.do_once4:
            self.payoff += 5
            self.do_once4 = False
        return self.quiz_1 == Const.answers[0]

    def is_donation_correct(self):
        if self.quiz_2 == Const.answers[1] and self.do_once3:
            self.do_once3 = False
            self.payoff += 5
        return self.quiz_2 == Const.answers[1]

    def is_both_Examples_right(self):
        if self.quiz_3a == Const.answers[2] \
            and self.quiz_3b == Const.answers[3] \
            and self.do_once:
            self.payoff += 5
            self.do_once = False
        return self.quiz_3a == Const.answers[2] and self.quiz_3b == Const.answers[3]

    def is_all_values_right(self):
        if self.do_once2 \
            and self.quiz_4a1 == Const.answers[4] \
            and self.quiz_4a2 == Const.answers[5] \
            and self.quiz_4a3 == Const.answers[6] \
            and self.quiz_4b1 == Const.answers[7] \
            and self.quiz_4b2 == Const.answers[8] \
            and self.quiz_4b3 == Const.answers[9]:
            self.payoff += 5
            self.do_once2 = False
        return self.quiz_4a1 == Const.answers[4] \
            and self.quiz_4a2 == Const.answers[5] \
            and self.quiz_4a3 == Const.answers[6] \
            and self.quiz_4b1 == Const.answers[7] \
            and self.quiz_4b2 == Const.answers[8] \
            and self.quiz_4b3 == Const.answers[9]

    def is_max_individual_correct(self):
        return self.quiz_3a == Const.answers[2]

    def is_max_group_correct(self):
        return self.quiz_3b == Const.answers[3]

    def display_instructions_again(self):
        display = self.in_round(Const.num_rounds / 2)
        return display.everything_correct

    def display_instructions(self):
        if self.round_number == 1:
            return True
        if self.round_number == Const.num_rounds / 2 + 1:
            return not self.display_instructions_again()
        return False

    def how_many_good_answers(self):
        counter = 0
        answers = [
            self.in_round(2).quiz_1 == Const.answers[0],
            self.in_round(2).quiz_2 == Const.answers[1],
            self.in_round(2).is_both_Examples_right(),
            self.in_round(2).is_all_values_right(),
        ]

        for answer_is_correct in answers:
            if answer_is_correct:
                counter += 5

        return c(counter)

    def total_pay(self):
        return self.group.bonus_in_dollars() \
            + self.remaining_tokens_in_dollars() \
            + c(5).to_real_world_currency(self.session) \
            + c(self.how_many_good_answers()).to_real_world_currency(self.session)


    # bot_contributions = [
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3],
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3]
    # ]
    # bot_contributions[round number][player number]
    # bot_total_contributions = [
    #     [10, 9, 8, 3, 3, 2, 2, 1, 8, 10, 10, 9, 8, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 4, 3],
    #     [20, 18, 16, 6, 6, 4, 4, 2, 16, 20, 20, 18, 16, 16, 14, 14, 12, 12, 12, 10, 10, 8, 8, 8, 6]
    # ]

    # PRACTICE AND REAL GAME
    payoff = 0

    contribution = models.CurrencyField(min=0, max=10)
    practice_contribution = models.CurrencyField(min=0, max=10)
    private_contribution = models.CurrencyField(min=0, max=10)
    practice_private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()
    bot_contributions_in_round = models.LongStringField()

    # QUIZES
    # ===========================================

    quiz_1 = models.StringField(
        label=Const.quiz_1_label,
        widget=widgets.RadioSelect
    )
    quiz_2 = models.StringField(
        label=Const.quiz_2_label,
        widget=widgets.RadioSelect
    )
    quiz_3a = models.StringField(
        label=Const.quiz_3a_label,
        widget=widgets.RadioSelect
    )
    quiz_3b = models.StringField(
        label=Const.quiz_3b_label,
        widget=widgets.RadioSelect
    )
    quiz_4a1 = models.StringField(
        label=Const.quiz_4a1_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$0.00",
            "$1.00",
            "$2.00"
        ]
    )
    quiz_4a2 = models.StringField(
        label=Const.quiz_4a2_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$6.00",
            "$8.00",
            "$16.00"
        ]
    )
    quiz_4a3 = models.StringField(
        label=Const.quiz_4a3_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$7.00",
            "$10.00",
            "$17.00"
        ]
    )
    quiz_4b1 = models.StringField(
        label=Const.quiz_4b1_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$0.00",
            "$1.00",
            "$2.00"
        ]
    )
    quiz_4b2 = models.StringField(
        label=Const.quiz_4b2_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$0.00",
            "$0.80",
            "$2.00"
        ]
    )
    quiz_4b3 = models.StringField(
        label=Const.quiz_4b3_label,
        widget=widgets.RadioSelectHorizontal,
        choices=[
            "$1.00",
            "$1.80",
            "$3.00"
        ]
    )

    timesInstruction1 = models.IntegerField(initial=0)
    timesInstruction2 = models.IntegerField(initial=0)
    timesInstruction3a = models.IntegerField(initial=0)
    timesInstruction3b = models.IntegerField(initial=0)
    timesInstruction4 = models.IntegerField(initial=0)

    repeatQuiz1 = models.BooleanField(initial=False)
    repeatQuiz2 = models.BooleanField(initial=False)
    repeatQuiz3a = models.BooleanField(initial=False)
    repeatQuiz3b = models.BooleanField(initial=False)
    repeatQuiz4 = models.BooleanField(initial=False)

    do_once = models.BooleanField(initial=True)
    do_once2 = models.BooleanField(initial=True)
    do_once3 = models.BooleanField(initial=True)
    do_once4 = models.BooleanField(initial=True)

    # SURVEY FORM FIELDS
    # ------------------
    # POST SURVEY 1a
    survey_goals = get_text_field(Const.survey_1_q1)
    survey_goals_success = get_yesno_field(Const.survey_1_q2)
    survey_guiding_info = get_text_field(Const.survey_1_q3)
    survey_individual_conservation = get_text_field(Const.survey_1_q4)
    survey_group_conservation = get_text_field(Const.survey_1_q5)

    # POST SURVEY 1b
    survey_rank_concentration = get_radiorange_field(Const.survey_1_qb1, Const.range_5, True)
    survey_rank_understandable = get_radiorange_field(Const.survey_1_qb2, Const.range_5, True)
    survey_rank_teamwork = get_radiorange_field(Const.survey_1_qb3, Const.range_5, True)
    survey_rank_group = get_radiorange_field(Const.survey_1_qb4, Const.range_5, True)
    survey_rank_collective = get_radiorange_field(Const.survey_1_qb5, Const.range_5, True)

    # POST SURVEY 1c
    survey_range_pastcontributions = get_radiorange_field(Const.survey_1_qc1, Const.range_5, True)
    survey_range_totalgroup = get_radiorange_field(Const.survey_1_qc2, Const.range_5, True)
    survey_range_totaloverall = get_radiorange_field(Const.survey_1_qc3, Const.range_5, True)
    survey_range_percentgoal = get_radiorange_field(Const.survey_1_qc4, Const.range_5, True)
    survey_range_envbenefit = get_radiorange_field(Const.survey_1_qc5, Const.range_5, True)



    # POST SURVEY 2
    survey_help_others = get_likert_field(Const.survey_2_items[0], Const.range_5)
    survey_share_ideas = get_likert_field(Const.survey_2_items[1], Const.range_5)
    survey_learn_others = get_likert_field(Const.survey_2_items[2], Const.range_5)
    survey_work_others = get_likert_field(Const.survey_2_items[3], Const.range_5)
    survey_self_best = get_likert_field(Const.survey_2_items[4], Const.range_5)
    survey_self_challenge = get_likert_field(Const.survey_2_items[5], Const.range_5)
    survey_dislike_teamwork = get_likert_field(Const.survey_2_items[6], Const.range_5)
    survey_bothered_teamwork = get_likert_field(Const.survey_2_items[7], Const.range_5)
    survey_better_alone = get_likert_field(Const.survey_2_items[8], Const.range_5)

    # POST_SURVEY 3
    survey_plants = get_likert_field(Const.survey_3_items[0], Const.range_concerned)
    survey_marinelife = get_likert_field(Const.survey_3_items[1], Const.range_concerned)
    survey_birds = get_likert_field(Const.survey_3_items[2], Const.range_concerned)
    survey_animals = get_likert_field(Const.survey_3_items[3], Const.range_concerned)
    survey_prosperity = get_likert_field(Const.survey_3_items[4], Const.range_concerned)
    survey_lifestyle = get_likert_field(Const.survey_3_items[5], Const.range_concerned)
    survey_health = get_likert_field(Const.survey_3_items[6], Const.range_concerned)
    survey_future = get_likert_field(Const.survey_3_items[7], Const.range_concerned)
    survey_community = get_likert_field(Const.survey_3_items[8], Const.range_concerned)
    survey_humanrace = get_likert_field(Const.survey_3_items[9], Const.range_concerned)
    survey_children = get_likert_field(Const.survey_3_items[10], Const.range_concerned)
    survey_unitedstates = get_likert_field(Const.survey_3_items[11], Const.range_concerned)

    # POST SURVEY 4
    survey_demographics_birthyear = get_int_field(Const.survey_4_items[0], 1900, 2020)
    survey_demographics_gender = get_select_field(Const.survey_4_items[1], Const.choice_demographics_gender)
    survey_demographics_ethnicity = get_select_field(Const.survey_4_items[2], Const.choices_demographics_ethnicity)
    survey_demographics_employment = get_select_field(Const.survey_4_items[3], Const.choices_demographics_employment)
    survey_demographics_experience = get_select_field(Const.survey_4_items[4], Const.choices_demographics_experience)
    survey_demographics_reliability = get_yesno_field(Const.survey_4_items[5])
    survey_demographics_political = get_select_field(Const.survey_4_items[6], Const.choices_demographics_political)
    survey_demographics_residency = get_int_field(Const.survey_4_items[7], 0, 120)
