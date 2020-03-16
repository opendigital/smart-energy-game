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
author = 'Matt Harris'
doc = """
RCODI Energy game Post Survey
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
    def creating_session(self):
        print('in creating_session', self.round_number)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # payoff = 0
    # contribution = models.CurrencyField(min=0, max=10)
    # practice_contribution = models.CurrencyField(min=0, max=10)
    # private_contribution = models.CurrencyField(min=0, max=10)
    # practice_private_contribution = models.CurrencyField(min=0, max=10)
    # random_others_contribution = models.CurrencyField()
    # group_random_total_contribution = models.CurrencyField()
    # bot_contributions_in_round = models.LongStringField()

    # SURVEY FORM FIELDS
    # ------------------
    survey_consent = models.BooleanField(
        label="",
        choices=[
            [True, 'Yes, I give my permission for the researchers to use my data.'] ,
            [False, 'No, I do not give permission for the researchers to use my data. Please discard the data you obtained from me.']
        ],
        widget=widgets.RadioSelect
    )

    # POST SURVEY 1
    s1a1 = get_text_field(Const.survey_1a_items[0])
    s1a2 = get_yesno_field(Const.survey_1a_items[1])
    s1a3 = get_text_field(Const.survey_1a_items[2])
    s1a4 = get_text_field(Const.survey_1a_items[3])
    s1a5 = get_text_field(Const.survey_1a_items[4])

    s1b1 = get_radiorange_field(Const.survey_1b_items[0], Const.range_5, True)
    s1b2 = get_radiorange_field(Const.survey_1b_items[1], Const.range_5, True)
    s1b3 = get_radiorange_field(Const.survey_1b_items[2], Const.range_5, True)
    s1b4 = get_radiorange_field(Const.survey_1b_items[3], Const.range_5, True)
    s1b5 = get_radiorange_field(Const.survey_1b_items[4], Const.range_5, True)

    s1c1 = get_radiorange_field(Const.survey_1c_items[0], Const.range_5, True)
    s1c2 = get_radiorange_field(Const.survey_1c_items[1], Const.range_5, True)
    s1c3 = get_radiorange_field(Const.survey_1c_items[2], Const.range_5, True)
    s1c4 = get_radiorange_field(Const.survey_1c_items[3], Const.range_5, True)
    s1c5 = get_radiorange_field(Const.survey_1c_items[4], Const.range_5, True)

    # POST SURVEY 2
    s2a0 = get_likert_field(Const.survey_2_items[0], Const.range_5)
    s2a1 = get_likert_field(Const.survey_2_items[1], Const.range_5)
    s2a2 = get_likert_field(Const.survey_2_items[2], Const.range_5)
    s2a3 = get_likert_field(Const.survey_2_items[3], Const.range_5)
    s2a4 = get_likert_field(Const.survey_2_items[4], Const.range_5)
    s2a5 = get_likert_field(Const.survey_2_items[5], Const.range_5)
    s2a6 = get_likert_field(Const.survey_2_items[6], Const.range_5)
    s2a7 = get_likert_field(Const.survey_2_items[7], Const.range_5)
    s2a8 = get_likert_field(Const.survey_2_items[8], Const.range_5)

    # POST SURVEY 3
    s3a0 = get_likert_field(Const.survey_3_items[0], Const.range_concerned)
    s3a1 = get_likert_field(Const.survey_3_items[1], Const.range_concerned)
    s3a2 = get_likert_field(Const.survey_3_items[2], Const.range_concerned)
    s3a3 = get_likert_field(Const.survey_3_items[3], Const.range_concerned)
    s3a4 = get_likert_field(Const.survey_3_items[4], Const.range_concerned)
    s3a5 = get_likert_field(Const.survey_3_items[5], Const.range_concerned)
    s3a6 = get_likert_field(Const.survey_3_items[6], Const.range_concerned)
    s3a7 = get_likert_field(Const.survey_3_items[7], Const.range_concerned)
    s3a8 = get_likert_field(Const.survey_3_items[8], Const.range_concerned)
    s3a9 = get_likert_field(Const.survey_3_items[9], Const.range_concerned)
    s3a10 = get_likert_field(Const.survey_3_items[10], Const.range_concerned)

    # POST SURVEY 4
    s4a1 = get_int_field(Const.survey_4_items[0], 1900, 2020)
    s4a2 = get_select_field(Const.survey_4_items[1], Const.choice_demographics_gender)
    s4a3 = get_select_field(Const.survey_4_items[2], Const.choices_demographics_ethnicity)
    s4a4 = get_select_field(Const.survey_4_items[3], Const.choices_demographics_employment)
    s4a5 = get_select_field(Const.survey_4_items[4], Const.choices_demographics_experience)
    s4a6 = get_yesno_field(Const.survey_4_items[5])
    s4a7 = get_select_field(Const.survey_4_items[6], Const.choices_demographics_political)
    s4a8 = get_int_field(Const.survey_4_items[7], 0, 120)
