from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Juan Camilo Cardenas Gomez'

doc = """
Solution for training problem
"""


class Constants(BaseConstants):
    name_in_url = 'training_problem'
    players_per_group = 22
    players_without_me = players_per_group - 1
    num_actual_rounds = 12 # edit this one
    num_rounds = num_actual_rounds + 1 # don't edit this one

    endowment = c(100)
    multiplier = 2

    group_goal = c(216)
    no_bonus = c(0)

    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']

    answers = ["6 tokens", "True", "True", "True","$1.00","$18.18","$19.18","$1.00","$0.00","$1.00"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_random_contribution = models.CurrencyField()
    bonus = models.CurrencyField(initial=c(0))
    doItOnce = models.BooleanField(initial=True)
    carbonFund = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])

        for p in self.get_players():
            if self.total_random_contribution:
                self.total_random_contribution = p.contribution + p.random_others_contribution

            p.payoff = c(10) - p.contribution

            if self.round_number == Constants.num_rounds:
                if Constants.group_goal <= self.all_rounds_contribution():
                    self.bonus = self.all_rounds_contribution() * Constants.multiplier / Constants.players_per_group
                    p.payoff += self.bonus

    # It's used for after-survey queries.
    def pay_quizzes(self):
        if self.doItOnce and self.round_number == Constants.num_rounds:
            self.doItOnce = False
            for p in self.get_players():
                p.payoff += p.how_many_good_answers()
        #return

    def pay_carbonfund(self):
        self.carbonFund = self.all_rounds_contribution()/10*22
        #return

    def all_rounds_contribution(self):
        return sum([g.total_contribution for g in self.in_rounds(2, self.round_number)])

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
    # PRACTICE AND REAL GAME
    contribution = models.CurrencyField(min=0, max=10)
    practice_contribution = models.CurrencyField(min=0, max=10)
    private_contribution = models.CurrencyField(min=0, max=10)
    practice_private_contribution = models.CurrencyField(min=0, max=10)
    random_others_contribution = models.CurrencyField()
    group_random_total_contribution = models.CurrencyField()

    # QUIZ
    Q1 = models.StringField(label='', widget=widgets.RadioSelectHorizontal)
    Q2 = models.StringField(label='', widget=widgets.RadioSelect)
    Q3a = models.StringField(label='', widget=widgets.RadioSelectHorizontal)
    Q3b = models.StringField(label='', widget=widgets.RadioSelectHorizontal)

    Q4a1 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$0.00", "$1.00", "$2.00"])
    Q4a2 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$18.18", "$20.18", "$22.18"])
    Q4a3 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$17.18", "$18.18", "$19.18"])
    Q4b1 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$0.00", "$1.00", "$2.00"])
    Q4b2 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$0.00", "$1.18", "$2.00"])
    Q4b3 = models.StringField(label='', widget=widgets.RadioSelectHorizontal,choices = ["$0.00", "$1.00", "$2.08"])

    repeatQuiz1 = models.BooleanField(initial=False)
    timesInstruction1 = models.IntegerField(initial=0)
    repeatQuiz2 = models.BooleanField(initial=False)
    timesInstruction2 = models.IntegerField(initial=0)
    repeatQuiz3a = models.BooleanField(initial=False)
    timesInstruction3a = models.IntegerField(initial=0)
    repeatQuiz3b = models.BooleanField(initial=False)
    timesInstruction3b = models.IntegerField(initial=0)
    repeatQuiz4 = models.BooleanField(initial=False)
    timesInstruction4 = models.IntegerField(initial=0)

    doItOnce = models.BooleanField(initial=True)
    doItOnce2 = models.BooleanField(initial=True)
    doItOnce3 = models.BooleanField(initial=True)
    doItOnce4 = models.BooleanField(initial=True)



    # POST SURVEY 1

    # I_like_to_help_other_people = models.StringField()
    # I_like_to_share_my_ideas_and_materials_with_others = models.StringField()
    # I_like_to_cooperate_with_others = models.StringField()
    # I_can_learn_important_things_from_others = models.StringField()
    # I_try_to_share_my_ideas_and_resources_with_others = models.StringField()
    # People_learn_lots_of_important_things_from_each_other = models.StringField()
    # It_is_a_good_idea_for_people_to_help_each_other = models.StringField()
    # I_like_to_do_better_work_than_others = models.StringField()
    # I_work_to_get_better_than_others = models.StringField()
    # I_like_to_be_the_best_at_what_I_do = models.StringField()
    # I_dont_like_to_be_second = models.StringField()
    # I_like_to_compete_with_other_students= models.StringField()
    # I_am_happiest_when_I_am_competing_with_others = models.StringField()
    # I_like_the_challenge_of_seeing_who_is_best = models.StringField()
    # Competing_with_others_is_a_good_way_to_work = models.StringField()
    # I_dont_like_working_with_others = models.StringField()
    # I_like_to_work_with_others_reverse = models.StringField()
    # It_bothers_me_when_I_have_to_work_with_others = models.StringField()
    # I_do_better_when_I_work_alone = models.StringField()
    # I_like_work_better_when_I_do_it_all_myself = models.StringField()
    # I_would_rather_work_along_than_with_others = models.StringField()
    # Working_in_small_groups_is_better_than_working_alone = models.StringField()

    # POST_SURVEY 2

    # Plants = models.StringField()
    # Marine_life = models.StringField()
    # Birds = models.StringField()
    # Animals = models.StringField()
    # My_prosperity = models.StringField()
    # My_lifestyle = models.StringField()
    # My_health = models.StringField()
    # My_future = models.StringField()
    # People_in_my_community = models.StringField()
    # The_human_race = models.StringField()
    # Children = models.StringField()
    # People_in_the_United_States = models.StringField()

    # POST_SURVEY 3
    birth = models.IntegerField()
    gender = models.StringField()
    ethnic_group = models.StringField()
    economic_status = models.StringField()
    previous_experiments = models.StringField()
    reliability = models.StringField()
    politic_party = models.StringField()
    years_in_us = models.IntegerField(min=0,max=120)

    # OPEN_QUESTIONS in POST_SURVEY 3
    early_conserve = models.StringField()
    middle_conserve = models.StringField()
    end_conserve = models.StringField()

    individual_conservation_feedback_rank = models.IntegerField()
    collective_conservation_feedback_rank = models.IntegerField()
    carbon_offset_feedback_rank = models.IntegerField()
    percent_goal_feedback_rank = models.IntegerField()
    total_contribution_feedback_rank = models.IntegerField()

    # WILD METHODS
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
        if self.round_number <= Constants.num_rounds/2:
            return sum([p.contribution for p in self.in_rounds(1, self.round_number-1)])
        else:
            return sum([p.contribution for p in self.in_rounds(Constants.num_rounds/2+1, self.round_number-1)])

    def others_contribution(self):
        return sum([p.contribution for p in self.get_others_in_group()])

    def others_contribution_array(self):
        return [p.contribution for p in self.get_others_in_group()]

    def all_rounds_others_contribution(self):
        return sum([p.all_rounds_contribution() for p in self.get_others_in_group()])

    def all_rounds_others_contribution_array(self):
        return ([p.all_rounds_contribution() for p in self.get_others_in_group()])

    def remaining_tokens_in_dollars(self):
        return c(self.all_tokens_left()).to_real_world_currency(self.session)

    def total_tokens_in_dollars(self):
        return self.remaining_tokens_in_dollars() + self.group.bonus_in_dollars()

    def total_contribution(self):
        if self.round_number <= Constants.num_rounds / 2:
            return sum([p.contribution for p in self.in_rounds(1, self.round_number - 1)])
        else:
            return sum([p.contribution for p in self.in_rounds(Constants.num_rounds / 2 + 1, self.round_number - 1)])

    def check_answers(self):
        if self.Q1 == Constants.answers[0] \
                and self.Q2 == Constants.answers[1] \
                and self.Q3a == Constants.answers[2] \
                and self.Q3b == Constants.answers[3]:
            self.everything_correct = True
            return True
        else:
            self.everything_correct = False
            return False

    def is_equilibrium_tokens_correct(self):
        if self.Q1 == Constants.answers[0] and self.doItOnce4:
            self.payoff += 5
            self.doItOnce4 = False
        return self.Q1 == Constants.answers[0]

    def is_donation_correct(self):
        if self.Q2 == Constants.answers[1] and self.doItOnce3:
            self.doItOnce3 = False
            self.payoff += 5
        return self.Q2 == Constants.answers[1]

    def is_both_Examples_right(self):
        if self.Q3a == Constants.answers[2] and self.Q3b == Constants.answers[3] and self.doItOnce :
            self.payoff += 5
            self.doItOnce = False
        return self.Q3a == Constants.answers[2] and self.Q3b == Constants.answers[3]

    def is_all_values_right(self):
        if self.doItOnce2 and self.Q4a1 == Constants.answers[4] and self.Q4a2 == Constants.answers[5] and self.Q4a3 == Constants.answers[6] and self.Q4b1 == Constants.answers[7] and self.Q4b2 == Constants.answers[8] and self.Q4b3 == Constants.answers[9]:
            self.payoff += 5
            self.doItOnce2 = False
        return self.Q4a1 == Constants.answers[4] and self.Q4a2 == Constants.answers[5] and self.Q4a3 == Constants.answers[6] and self.Q4b1 == Constants.answers[7] and self.Q4b2 == Constants.answers[8] and self.Q4b3 == Constants.answers[9]

    def is_max_individual_correct(self):
        return self.Q3a == Constants.answers[2]

    def is_max_group_correct(self):
        return self.Q3b == Constants.answers[3]

    def display_instructions_again(self):
        display = self.in_round(Constants.num_rounds / 2)
        return display.everything_correct

    def display_instructions(self):
        if self.round_number == 1:
            return True
        elif self.round_number == Constants.num_rounds/2+1:
            return not self.display_instructions_again()
        else:
            return False

    def how_many_good_answers(self):
        counter = 0
        answers = [
                   self.in_round(2).Q1 == Constants.answers[0],
                   self.in_round(2).Q2 == Constants.answers[1],
                   self.in_round(2).is_both_Examples_right(),
                   self.in_round(2).is_all_values_right(),
                   ]
        for answer_is_correct in answers:
            if answer_is_correct:
                counter+=5

        return c(counter)

    def total_pay(self):
        return self.group.bonus_in_dollars() + self.remaining_tokens_in_dollars() + c(5).to_real_world_currency(self.session) + c(self.how_many_good_answers()).to_real_world_currency(self.session)
