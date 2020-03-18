from os import environ


# ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
# ADMIN_PASSWORD = 'GoBoilers2018!'
# OTREE_PRODUCTION Consider '', None, and '0' to be empty/false
# SENTRY_DSN = environ.get('SENTRY_DSN')
# AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'
AUTH_LEVEL = 'DEMO'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'
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


mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
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
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
        'name': 'main',
        'display_name': "MAIN: Full Game",
        'num_demo_participants': 1,
        'app_sequence': ['onboarding_app' ,'energy_game', 'post_game']
    },
    {
        'name': 'onboarding',
        'display_name': "Section | ONBOARDING: Teach and Practice Module",
        'num_demo_participants': 1,
        'app_sequence': ['onboarding_app'],
    },
    {
        'name': 'energy_game',
        'display_name': "Section | GAMEPLAY: Conservation Energy (Game Rounds Only)",
        'num_demo_participants': 1,
        'app_sequence': ['energy_game'],
    },
    {
        'name': 'post_game',
        'display_name': "Section | EXIT SURVEY: Post-Game Survey",
        'num_demo_participants': 1,
        'app_sequence': ['post_game'],
    }
]


DEMO_PAGE_INTRO_HTML = """
In order to test
</br>
USER: admin</br>
PASS: admin
</br></br>
"""
