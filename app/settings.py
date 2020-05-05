from os import environ

# OTREE_PRODUCTION Consider '', None, and '0' to be empty/false
# SENTRY_DSN = environ.get('SENTRY_DSN')
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
# POINTS_CUSTOM_NAME = 'tokens'
# BROWSER_COMMAND = ''

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
OTREE_PRODUCTION='1'
# ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
# ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME')
ADMIN_USERNAME = 'developer'
ADMIN_PASSWORD = 'developer'
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
# DEBUG = False
DEBUG = True
POINTS_CUSTOM_NAME = 'tokens'
AUTH_LEVEL = 'DEMO'
# AUTH_LEVEL = 'STUDY'
SECRET_KEY = '68j-5$9@d=m0_*pb0n=_3u6%33fng(738yww&w^ttk136n(4vz'
INSTALLED_APPS = [
    'otree',
]

ROOMS = [{
    'name': 'test_in_progress',
    'display_name': 'Testing In Progress',
    'participant_label_file': '_rooms/test_room.txt',
}, {
    'name': 'live_demo',
    'display_name': 'Room for live demo (no participant labels)',
}]

MTURK_HIT_SETTINGS = {
    'keywords': ['bonus', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'template': 'global/mturk_template.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,
    'grant_qualification_id': '31QNOLHLAC6NIMX6DIG1ZLVNCV9IMY',
    'qualification_requirements': [{
        'QualificationTypeId': "31QNOLHLAC6NIMX6DIG1ZLVNCV9IMY",
        'Comparator': "DoesNotExist",
    }]
}


SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 0.50,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'main',
        'display_name': "MAIN: Main Game Sequnce",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey'],
    },
    {
        'name': 'mturk',
        'display_name': "MTURK: Main Game (mturk)",
        'num_demo_participants': 1,
        'app_sequence': ['quiz', 'game', 'survey'],
        'mturk_hit_settings': MTURK_HIT_SETTINGS,
    },
    # {
    #     'name': 'quiz',
    #     'display_name': "QUIZ: Pregame Training and Practice",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['quiz'],
    # },
    {
        'name': 'game',
        'num_demo_participants': 1,
        'wait_for_all_groups': False,
        'display_name': "GAME:  Energy Conservation Game",
        'app_sequence': ['game'],
    },
    # {
    #     'name': 'survey',
    #     'display_name': "SURVEY: Postgame Survey",
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
In order to test
</br>
</br>
</br>
"""
