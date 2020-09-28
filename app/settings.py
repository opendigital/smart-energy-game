from os import environ

# OTREE_PRODUCTION Consider '', None, and '0' to be empty/false
# SENTRY_DSN = environ.get('SENTRY_DSN')
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
# POINTS_CUSTOM_NAME = 'tokens'
# BROWSER_COMMAND = ''

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
OTREE_PRODUCTION='1'
LANGUAGE_CODE = 'en'
# ADMIN_USERNAME = 'developer'
# ADMIN_PASSWORD = 'developer'
ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEBUG = False
# DEBUG = True
POINTS_CUSTOM_NAME = 'tokens'
# AUTH_LEVEL = 'DEMO'
AUTH_LEVEL = 'STUDY'
SECRET_KEY = '68j-5$9@d=m0_*pb0n=_3u6%33fng(738yww&w^ttk136n(4vz'
INSTALLED_APPS = [
    "otree",
]

ROOMS = [{
    "name": "test_in_progress",
    "display_name": "Testing In Progress",
    "participant_label_file": "_rooms/test_room.txt",
}, {
    "name": "live_demo",
    "display_name": "Room for live demo (no participant labels)",
}]

MTURK_HIT_SETTINGS = {
    "keywords": [
        "energy conservation game",
        "real-word impact",
        "carbon offset",
        "donation task",
        "trade-offs",
        "bonus",
    ],
    "title": "Multiplayer energy conservation game with real-world impact",
    "description": "The purpose of this research is to learn about how people make energy related decisions. We plan to recruit up to 1,000 participants. The study will last no more than 60 minutes and your pay will vary depending on your and other's decisions during the game.",
    "frame_height": 500,
    "template": "global/mturk_template.html",
    "minutes_allotted_per_assignment": 60,
    "expiration_hours": 7 * 24,
    "grant_qualification_id": "3T0EA825IJO4BK6G2YOU4KNLRVSQQ3",
    "qualification_requirements": [
        {
            "QualificationTypeId": "3T0EA825IJO4BK6G2YOU4KNLRVSQQ3",
            "Comparator": "DoesNotExist",
        },
        {
            "QualificationTypeId": "00000000000000000071",
            "Comparator": "EqualTo",
            "LocaleValues":[{
                "Country": "US"
            }]
        }
    ]
}


SESSION_CONFIG_DEFAULTS = {
    "real_world_currency_per_point": 0.01,
    "participation_fee": 0.50,
    "doc": "",
    "game_type": "base"
}

SESSION_CONFIGS = [
    {
        'name': 'base_game',
        'display_name': "Base Game",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'base',
    },
    {
        'name': 'descriptive_text_game',
        'display_name': " Text Game - Descriptive Norm",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'descriptive_text',
    },
    {
        'name': 'injunctive_text_game',
        'display_name': "Text Game - Injunctive Norm",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'injunctive_text',
    },
    {
        'name': 'radial_visual_game',
        'display_name': "Visual Game - Radial Charts",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'visual_game',
    },
    {
        'name': 'mturk_base_game',
        'display_name': "MTurk: Base Game",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'base',
        'mturk_hit_settings': MTURK_HIT_SETTINGS,
    },
    {
        'name': 'mturk_descriptive_text',
        'display_name': "MTurk: Text Game - Descriptive Norm",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'descriptive_text',
        'mturk_hit_settings': MTURK_HIT_SETTINGS,
    },
    {
        'name': 'mturk_injunctive_text',
        'display_name': "MTurk: Text Game - Injunctive Norm",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'injunctive_text',
        'mturk_hit_settings': MTURK_HIT_SETTINGS,
    },
    {
        'name': 'mturk_radial_visual_game',
        'display_name': "MTurk: Visual Game - Radial Charts",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey', 'results'],
        'game_type': 'visual_game',
        'mturk_hit_settings': MTURK_HIT_SETTINGS,
    },
    # {
    #     'name': 'game_only',
    #     'num_demo_participants': 1,
    #     'wait_for_all_groups': False,
    #     'display_name': "GAME ONLY:  Energy Conservation Game",
    #     'game_type': 'base_game',
    #     'app_sequence': ['game'],
    # },
    # {
    #     'name': 'quiz',
    #     'display_name': "QUIZ ONLY: Pregame Training and Practice",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['quiz'],
    # },
    # {
    #     'name': 'survey',
    #     'display_name': "SURVEY ONLY: Postgame Survey",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['survey'],
    # },
    # {
    #     'name': 'nogame',
    #     'display_name': "NO_GAME: Content Tests",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['quiz', 'survey'],
    # }
]


DEMO_PAGE_INTRO_HTML = """
RCODI Energy Game
</br>
</br>
</br>
"""
