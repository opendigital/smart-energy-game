from os import environ

SENTRY_DSN = environ.get('SENTRY_DSN')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'

# AUTH_LEVEL:
# - If not set (default), whole site is freely accessible
# - If launching a study and want visitors to only be able play your app
#   if provided a start link, set it to STUDY
# - If site will be = online in public demo mode, anybody can play a
#   demo version of your game, but not access the the admin interface, set to DEMO
# you can set the AUTH_LEVEL using the environment variable `OTREE_AUTH_LEVEL`
# for security, best to set admin password with the environment variable `OTREE_ADMIN_PASSWORD`

# ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
# ADMIN_PASSWORD = 'GoBoilers2018!'
# OTREE_PRODUCTION Consider '', None, and '0' to be empty/false


DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

AUTH_LEVEL = 'DEMO'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

#SECRET_KEY don't share this with anybody.
SECRET_KEY = '68j-5$9@d=m0_*pb0n=_3u6%33fng(738yww&w^ttk136n(4vz'

# if an app is included in SESSION_CONFIGS, you don't need to list it here

INSTALLED_APPS = ['otree']

DEMO_PAGE_INTRO_HTML = """
In order to test
</br>
USER: admin</br>
PASS: admin
</br></br>

"""

ROOMS = [{
    'name': 'econ101',
    'display_name': 'Econ 101 class',
    'participant_label_file': '_rooms/econ101.txt',
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
        'name': 'main_app',
        'display_name': "Energy Conservation Game",
        'num_demo_participants': 1,
        'app_sequence': ['main_app']
    },
    # {
    #     'name': 'real_effort',
    #     'display_name': "Real-effort transcription task",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['real_effort'],
    # },
    # {
    #     'name': 'quiz',
    #     'display_name': "Quiz",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['quiz'],
    # }
]
