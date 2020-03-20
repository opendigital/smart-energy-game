import random
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

        print("self.round_number", self.round_number)
        print("MONTH", round_month)
        print("index", index)
        return {
            'page_title': 'Energy Game',
            'current_month': round_month,
            'current_round': self.round_number,
            'progress': 'Game'
        }


class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    # models.Player.bot_contributions =\
    #    [[10 for x in round_] for round_ in models.Player.bot_contributions]
    # print(models.Player.bot_contributions)

    def is_displayed(self):
        return self.round_number >= 1

    def before_next_page(self):
        self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
        print("test")

    # self.models.player.bot_contributions =\
    #   [[10 for x in round_] for round_ in self.player.bot_contributions]
    # print(self.models.group.bot_contributions)

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.set_bots()



class Results(Page):
    def is_displayed(self):
        return self.round_number >= 1

    # def before_next_page(self):
    #     self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
    #     print("test")

    def vars_for_template(self):
        # Utils.dump_obj(self.player, 'player')
        # Utils.dump_obj(self.session, 'session')
        Utils.dump_obj(self.group, 'group')
        print('get_total_contribution', self.group.get_total_contribution())
        print('self.group.get_avg_contribution()', self.group.get_avg_contribution())
        index = self.round_number - 1
        round_month = Utils.get_month(index)
        return {
            'page_title': 'Energy Game Results',
            'others_contribution': self.player.others_contribution,
            'total_contribution': self.group.get_total_contribution(),
            'avg_contrib': str(self.group.get_avg_contribution()),
            'current_month': round_month,
            'current_round': self.round_number,
            'progress': 'Game'
        }


class Congrats(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        # let today = new Date();
        # 'cert_date': ,
        return {
            'page_title': 'Your Group\'s Air Pollution Reduction Result',
            'all_rounds_others_contribution': self.player.all_rounds_others_contribution(),
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'progress': 'Game',
            'lbs': str(self.group.all_rounds_contribution()/10*22).split(" ")[0] + " lbs",
            'amount': c(self.group.all_rounds_contribution()).to_real_world_currency(self.session)
        }


class FinalResults(Page):

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        Utils.dump_obj(self.player._state, 'player_state')
        Utils.dump_obj(self.player.participant, 'participant')
        return {
            'page_title': 'Energy Game Results',
            'progress': 'Game',
            'js_vars': str(self.participant.vars),
            'current_month': Constants.MONTHS[(self.round_number - 2) % 12],
            'current_round': self.round_number - 1,
            'goal_meet': Constants.group_goal <= self.group.all_rounds_contribution(),
            'carbonfund': self.group.all_rounds_contribution_in_dollars(),
            'quiz': c(self.player.how_many_good_answers()).to_real_world_currency(self.session)
        }


    def before_next_page(self):
        self.player.participant_vars_dump = str(self.participant.vars)
        self.group.pay_carbonfund()
        self.group.pay_quizzes()


page_sequence = [
    Game,
    ResultsWaitPage,
    Results,
    Congrats,
    FinalResults,
]
