from random import shuffle
from otree.api import Currency as c
from ._builtin import Page
from .constants import Constants



class SurveyIntro(Page):
    def vars_for_template(self):
        return {
            'page_title': 'Survey Introduction',
            'progress': 'Survey'
        }



class PostSurvey1(Page):
    form_model = 'player'
    form_fields = [
        's1a1',
        's1a2',
        's1a3',
        's1a4',
        's1a5',
        's1b1',
        's1b2',
        's1b3',
        's1b4',
        's1b5',
        's1c1',
        's1c2',
        's1c3',
        's1c4',
        's1c5',
    ]

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["PostSurvey1"],
            'progress': 'Survey'
        }

    def before_next_page(self):
        self.player.payout_page()


class PostSurvey2(Page):
    form_model = 'player'
    form_fields = [
        's2a0',
        's2a1',
        's2a2',
        's2a3',
        's2a4',
        's2a5',
        's2a6',
        's2a7',
        's2a8',
    ]

    def get_form_fields(self):
        fields = [
            's2a0',
            's2a1',
            's2a2',
            's2a3',
            's2a4',
            's2a5',
            's2a6',
            's2a7',
            's2a8',
        ]
        shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["PostSurvey2"],
            'progress': 'Survey',
        }

    def before_next_page(self):
        self.player.payout_page()

class PostSurvey3(Page):
    """Page Docstring"""
    form_model = 'player'
    form_fields = [
        's3a0',
        's3a1',
        's3a2',
        's3a3',
        's3a4',
        's3a5',
        's3a6',
        's3a7',
        's3a8',
        's3a9',
        's3a10',
    ]

    def get_form_fields(self):
        fields = [
            's3a0',
            's3a1',
            's3a2',
            's3a3',
            's3a4',
            's3a5',
            's3a6',
            's3a7',
            's3a8',
            's3a9',
            's3a10',
        ]
        shuffle(fields)
        return fields

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["PostSurvey3"],
            'progress': 'Survey',
        }

    def before_next_page(self):
        self.player.payout_page()



class PostSurvey4(Page):
    form_model = 'player'
    form_fields = [
        's4a1',
        's4a2',
        's4a3',
        's4a4',
        's4a5',
        's4a6',
        's4a7',
        's4a8',
    ]

    def vars_for_template(self):
        return {
            'page_title': Constants.page_titles["PostSurvey4"],
            'progress': 'Survey',
        }

    def before_next_page(self):
        self.player.payout_page()
        self.player.finalize_game_survey_data()



page_sequence = [
    SurveyIntro,
    PostSurvey1,
    PostSurvey2,
    PostSurvey3,
    PostSurvey4,
]
