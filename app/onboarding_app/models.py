import json
import inspect
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .constants import Constants

AUTHOR = 'Matt Harris'

DOC = """
RCODI Energy Game Pre-game training
"""


# _ Session
# num_participants
# config
# vars

class Subsession(BaseSubsession):
    # BUILTIN:
    # __ session
    # __ round_number
    # __ creating_session()
    # __ get_groups()
    # __ get_players()
    # __ group_randomly()
    # __ group_like_round()
    # __ get_group_matrix()
    # __ set_group_matrix()
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)

    def get_quiz_group(self, index):
        return [
            Constants.q1,
            Constants.q2,
            Constants.q3,
            Constants.q4
        ][index]

    def get_keys_from_quiz_group(self, index):
        answers = []
        group = self.get_quiz_group(index)
        for field in group:
            answers.append(field["answer"])
        return answers

    def get_all_keys_from_quiz_group(self):
        return [
            self.get_keys_from_quiz_group(0),
            self.get_keys_from_quiz_group(1),
            self.get_keys_from_quiz_group(2),
            self.get_keys_from_quiz_group(3),
        ]

    def review_rulepage(self):
        print('review_rulepage')
        return []

    def set_quizdata(self):
        return dict(
            q1=0,
            q2=0,
            q3a=0,
            q3b=0,
            q4a=0,
            q4b=0,
            q4c=0,
            q4d=0,
            q4e=0,
            q4f=0,
        )

    def creating_session(self):
        print('init session', self.round_number)
        session_answers = self.get_all_keys_from_quiz_group()
        self.session.vars["answer_key"] = session_answers
        for p in self.get_players():
            p.payoff = c(0)
            p.participant.vars["qattempts"] = self.set_quizdata()
            p.participant.vars["qcorrect"] = self.set_quizdata()



class Group(BaseGroup):
    # BUILTIN:
    # __ session/subsession
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)
    # __ get_player_by_role(role)
    # __ get_player_by_id(id_in_group)
    # __ get_players()
    pass


# _ Participant
# id_in_session
# vars
# label
# payoff
# payoff_plus_participation_fee
#
class Player(BasePlayer):
    # BUILTIN:
    # __ payoff
    # __ session/subsession/group/participant
    # __ id_in_group
    # __ role()
    # __ in_all_rounds()
    # __ in_previous_rounds()
    # __ in_rounds(first, last)
    # __ in_round(round_number)
    # __ get_others_in_subsession()
    # __ get_others_in_group()


    quiz_result = models.LongStringField()
    review_rules = models.IntegerField(initial=0)
    practice_contribution = models.CurrencyField(min=0, max=10)

    def qattempts(self, q):
        return self.participant.vars["qattempts"][q]

    def bump_qattempt(self, q):
        self.participant.vars["qattempts"][q] += 1

    def qcorrect(self, q):
        return self.participant.vars["qcorrect"][q] == 1

    def set_qcorrect(self, q, value):
        self.participant.vars["qcorrect"][q] = value

    def finalize_data(self):
        result=dict(
            correct=[
                self.participant.vars["qcorrect"]["q1"],
                self.participant.vars["qcorrect"]["q2"],
                self.participant.vars["qcorrect"]["q3a"],
                self.participant.vars["qcorrect"]["q3b"],
                self.participant.vars["qcorrect"]["q4a"],
                self.participant.vars["qcorrect"]["q4b"],
                self.participant.vars["qcorrect"]["q4c"],
                self.participant.vars["qcorrect"]["q4d"],
                self.participant.vars["qcorrect"]["q4e"],
                self.participant.vars["qcorrect"]["q4f"],
            ],
            attempts=[
                self.participant.vars["qattempts"]["q1"],
                self.participant.vars["qattempts"]["q2"],
                self.participant.vars["qattempts"]["q3a"],
                self.participant.vars["qattempts"]["q3b"],
                self.participant.vars["qattempts"]["q4a"],
                self.participant.vars["qattempts"]["q4b"],
                self.participant.vars["qattempts"]["q4c"],
                self.participant.vars["qattempts"]["q4d"],
                self.participant.vars["qattempts"]["q4e"],
                self.participant.vars["qattempts"]["q4f"],
            ],
            bonus=self.payoff,
        )
        self.quiz_result = str(result)
        self.participant.vars["quiz_result"] = str(result)
        print(str(result))

    def quiz_bonus(self):
        self.payoff += 5

    def dump_participant_vars(self):
        self.player.participant_vars_dump = str(self.participant.vars)

    def all_rounds_group_random_contribution(self):
        return sum([p.group_random_total_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_random_contribution(self):
        return sum([p.random_others_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_contribution(self):
        return sum([p.practice_contribution for p in self.in_rounds(1, self.round_number)])

    def all_rounds_practice_private_contribution(self):
        return sum([p.practice_private_contribution for p in self.in_rounds(1, self.round_number)])


    def valid_q1(self, values):
        if self.qcorrect("q1"):
            return True

        quiz_index = 0
        answers = self.session.vars["answer_key"][quiz_index]
        self.bump_qattempt("q1")

        if self.q1 == answers[0] or values["q1"] == answers[0]:
            self.set_qcorrect("q1", 1)
            if self.qattempts("q1") <= 2:
                self.quiz_bonus()
            return True
        else:
            return False


    def valid_q2(self, values):
        if self.qcorrect("q2"):
            return True

        quiz_index = 1
        answers = self.session.vars["answer_key"][quiz_index]
        self.bump_qattempt("q2")

        if self.q2 == answers[0] or values["q2"] == answers[0]:
            self.set_qcorrect("q2", 1)

            if self.qattempts("q2") <= 2:
                self.quiz_bonus()
            return True
        else:
            return False


    def valid_q3(self, values):
        quiz_index = 2
        answers = self.session.vars["answer_key"][quiz_index]

        if self.qcorrect("q3a") is not True:
            self.bump_qattempt("q3a")
            if self.q3a == answers[0] or values["q3a"] == answers[0]:
                self.set_qcorrect("q3a", 1)


        if self.qcorrect("q3b") is not True:
            self.bump_qattempt("q3b")
            if self.q3b == answers[1] or values["q3b"] == answers[1]:
                self.set_qcorrect("q3b", 1)

        if self.qcorrect("q3a") and self.qcorrect("q3b"):
            if self.qattempts("q3a") <= 2:
                self.quiz_bonus()
            return True
        return False



    def q4_total_attempts(self):
        return self.qattempts("q4a") \
            + self.qattempts("q4b") \
            + self.qattempts("q4c") \
            + self.qattempts("q4d") \
            + self.qattempts("q4e") \
            + self.qattempts("q4f")

    def valid_q4(self, values):
        quiz_index = 3
        answers = self.session.vars["answer_key"][quiz_index]

        if self.qcorrect("q4a") is not True:
            self.bump_qattempt("q4a")
            if self.q4a == answers[0] or values["q4a"] == answers[1]:
                self.set_qcorrect("q4a", 1)

        if self.qcorrect("q4b") is not True:
            self.bump_qattempt("q4b")
            if self.q4b == answers[1] or values["q4b"] == answers[1]:
                self.set_qcorrect("q4b", 1)

        if self.qcorrect("q4c") is not True:
            self.bump_qattempt("q4c")
            if self.q4c == answers[2] or values["q4c"] == answers[2]:
                self.set_qcorrect("q4c", 1)

        if self.qcorrect("q4d") is not True:
            self.bump_qattempt("q4d")
            if self.q4d == answers[3] or values["q4d"] == answers[3]:
                self.set_qcorrect("q4d", 1)

        if self.qcorrect("q4e") is not True:
            self.bump_qattempt("q4e")
            if self.q4e == answers[4] or values["q4e"] == answers[4]:
                self.set_qcorrect("q4e", 1)

        if self.qcorrect("q4f") is not True:
            self.bump_qattempt("q4f")
            if self.q4f == answers[5] or values["q4f"] == answers[5]:
                self.set_qcorrect("q4f", 1)

        correct = self.participant.vars["qcorrect"]
        sum = 0 + correct["q4a"] + correct["q4b"] \
            + correct["q4c"] + correct["q4d"] \
            + correct["q4e"] + correct["q4f"]

        if sum == 6 and self.qattempts("q4a") <= 2:
            self.quiz_bonus()
            return True

        return [
            self.qcorrect("q4a"),
            self.qcorrect("q4b"),
            self.qcorrect("q4c"),
            self.qcorrect("q4d"),
            self.qcorrect("q4e"),
            self.qcorrect("q4f"),
         ]



    # QUIZES
    # ===========================================
    q1 = models.IntegerField(
        label=Constants.q1[0]["label"],
        choices=Constants.q1[0]["choices"],
        widget=widgets.RadioSelect,
    )

    q2 = models.BooleanField(
        label=Constants.q2[0]["label"],
        choices=Constants.q2[0]["choices"],
        widget=widgets.RadioSelect
    )

    q3a = models.BooleanField(
        label=Constants.q3[0]["label"],
        choices=Constants.q3[0]["choices"],
        widget=widgets.RadioSelect,
    )

    q3b = models.BooleanField(
        label=Constants.q3[1]["label"],
        choices=Constants.q3[1]["choices"],
        widget=widgets.RadioSelect
    )

    q4a = models.IntegerField(
        label=Constants.q4[0]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[0]["choices"]
    )

    q4b = models.IntegerField(
        label=Constants.q4[1]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[1]["choices"]
    )

    q4c = models.IntegerField(
        label=Constants.q4[2]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[2]["choices"]
    )

    q4d = models.IntegerField(
        label=Constants.q4[3]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[3]["choices"]
    )

    q4e = models.IntegerField(
        label=Constants.q4[4]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[4]["choices"]
    )

    q4f = models.IntegerField(
        label=Constants.q4[5]["label"],
        widget=widgets.RadioSelectHorizontal,
        choices=Constants.q4[5]["choices"]
    )
