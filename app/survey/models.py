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

_c_ = Constants

author = 'Matt Harris'
doc = """
RCODI Energy Game Post Survey
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


def get_selectint_field(_label, _choices):
    """Return otree select field type"""
    return models.IntegerField(
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
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    survey_payout = models.IntegerField(initial=0)

    # POST SURVEY 1
    s1a1 = get_text_field(_c_.survey_1a_items[0])
    s1a2 = get_yesno_field(_c_.survey_1a_items[1])
    s1a3 = get_text_field(_c_.survey_1a_items[2])
    s1a4 = get_text_field(_c_.survey_1a_items[3])
    s1a5 = get_text_field(_c_.survey_1a_items[4])

    s1b1 = get_radiorange_field(_c_.survey_1b_items[0], _c_.range_5, True)
    s1b2 = get_radiorange_field(_c_.survey_1b_items[1], _c_.range_5, True)
    s1b3 = get_radiorange_field(_c_.survey_1b_items[2], _c_.range_5, True)
    s1b4 = get_radiorange_field(_c_.survey_1b_items[3], _c_.range_5, True)
    s1b5 = get_radiorange_field(_c_.survey_1b_items[4], _c_.range_5, True)

    s1c1 = get_radiorange_field(_c_.survey_1c_items[0], _c_.range_5, True)
    s1c2 = get_radiorange_field(_c_.survey_1c_items[1], _c_.range_5, True)
    s1c3 = get_radiorange_field(_c_.survey_1c_items[2], _c_.range_5, True)
    s1c4 = get_radiorange_field(_c_.survey_1c_items[3], _c_.range_5, True)
    s1c5 = get_radiorange_field(_c_.survey_1c_items[4], _c_.range_5, True)

    # POST SURVEY 2
    s2a0 = get_likert_field(_c_.survey_2_items[0], _c_.range_5)
    s2a1 = get_likert_field(_c_.survey_2_items[1], _c_.range_5)
    s2a2 = get_likert_field(_c_.survey_2_items[2], _c_.range_5)
    s2a3 = get_likert_field(_c_.survey_2_items[3], _c_.range_5)
    s2a4 = get_likert_field(_c_.survey_2_items[4], _c_.range_5)
    s2a5 = get_likert_field(_c_.survey_2_items[5], _c_.range_5)
    s2a6 = get_likert_field(_c_.survey_2_items[6], _c_.range_5)
    s2a7 = get_likert_field(_c_.survey_2_items[7], _c_.range_5)
    s2a8 = get_likert_field(_c_.survey_2_items[8], _c_.range_5)

    # POST SURVEY 3
    s3a0 = get_likert_field(_c_.survey_3_items[0], _c_.range_concerned)
    s3a1 = get_likert_field(_c_.survey_3_items[1], _c_.range_concerned)
    s3a2 = get_likert_field(_c_.survey_3_items[2], _c_.range_concerned)
    s3a3 = get_likert_field(_c_.survey_3_items[3], _c_.range_concerned)
    s3a4 = get_likert_field(_c_.survey_3_items[4], _c_.range_concerned)
    s3a5 = get_likert_field(_c_.survey_3_items[5], _c_.range_concerned)
    s3a6 = get_likert_field(_c_.survey_3_items[6], _c_.range_concerned)
    s3a7 = get_likert_field(_c_.survey_3_items[7], _c_.range_concerned)
    s3a8 = get_likert_field(_c_.survey_3_items[8], _c_.range_concerned)
    s3a9 = get_likert_field(_c_.survey_3_items[9], _c_.range_concerned)
    s3a10 = get_likert_field(_c_.survey_3_items[10], _c_.range_concerned)

    # POST SURVEY 4
    s4a1 = get_int_field(_c_.survey_4_items[0], 1900, 2020)
    s4a2 = get_selectint_field(_c_.survey_4_items[1], _c_.choice_demographics_gender)
    s4a3 = get_selectint_field(_c_.survey_4_items[2], _c_.choices_demographics_ethnicity)
    s4a4 = get_selectint_field(_c_.survey_4_items[3], _c_.choices_demographics_employment)
    s4a5 = get_selectint_field(_c_.survey_4_items[4], _c_.choices_demographics_experience)
    s4a6 = get_yesno_field(_c_.survey_4_items[5])
    s4a7 = get_selectint_field(_c_.survey_4_items[6], _c_.choices_demographics_political)
    s4a8 = get_int_field(_c_.survey_4_items[7], 0, 120)

    def payout_page(self):
        self.payoff += 5
        self.survey_payout += 5

    def finalize_game_survey_data(self):
        self.participant.vars["survey_payout"] = self.survey_payout
