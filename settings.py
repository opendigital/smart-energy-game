from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

# Environment keys for AWS
SENTRY_DSN = environ.get('SENTRY_DSN')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    'grant_qualification_id': '31QNOLHLAC6NIMX6DIG1ZLVNCV9IMY',
    'qualification_requirements': [
        {
            'QualificationTypeId': "31QNOLHLAC6NIMX6DIG1ZLVNCV9IMY",
            'Comparator': "DoesNotExist",
        }
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.10,
    'participation_fee': 0.50,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,  # Line for Mturk config
}

SESSION_CONFIGS = [
    {
        'name': 'descriptive',
        'display_name': "Descriptive (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['descriptive']
    },
    {
        'name': 'visualp',
        'display_name': "Partial Animated Proximity Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualp'],
    },
    {
        'name': 'visualpfull',
        'display_name': "Full Animated Proximity Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualpfull'],
    },
    {
        'name': 'visualpnoanim',
        'display_name': "Partial Non-Animated Proximity Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualpnoanim'],
    },
    {
        'name': 'visualpfullnoanim',
        'display_name': "Full Non-Animated Proximity Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualpfullnoanim'],
    },
    {
        'name': 'visualr',
        'display_name': "Partial Animated Radial Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualr'],
    },
    {
        'name': 'visualrfull',
        'display_name': "Full Animated Radial Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualrfull'],
    },
    {
        'name': 'visualrnoanim',
        'display_name': "Partial Non-Animated Radial Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualrfullnoanim'],
    },
    {
        'name': 'visualrfullnoanim',
        'display_name': "Full Non-Animated Radial Chart (12 rounds)",
        'num_demo_participants': 3,
        'app_sequence': ['visualrfullnoanim'],
    },
]
# see the end of this file for the inactive session configs


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = 'DEMO'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'GoBoilers2018!'  # environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
In order to test 

USER:admin
PASSWORD:GoBoilers2018!


"""

# don't share this with anybody.
SECRET_KEY = '68j-5$9@d=m0_*pb0n=_3u6%33fng(738yww&w^ttk136n(4vz'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# inactive session configs
# {
# 'name': 'trust',
# 'display_name': "Trust Game",
# 'num_demo_participants': 2,
# 'app_sequence': ['trust', 'payment_info'],
# },
# {
# 'name': 'prisoner',
# 'display_name': "Prisoner's Dilemma",
# 'num_demo_participants': 2,
# 'app_sequence': ['prisoner', 'payment_info'],
# },
# {
# 'name': 'ultimatum',
# 'display_name': "Ultimatum (randomized: strategy vs. direct response)",
# 'num_demo_participants': 2,
# 'app_sequence': ['ultimatum', 'payment_info'],
# },
# {
# 'name': 'ultimatum_strategy',
# 'display_name': "Ultimatum (strategy method treatment)",
# 'num_demo_participants': 2,
# 'app_sequence': ['ultimatum', 'payment_info'],
# 'use_strategy_method': T'rcodibasegame2018'#rue,
# },
# {
# 'name': 'ultimatum_non_strategy',
# 'display_name': "Ultimatum (direct response treatment)",
# 'num_demo_participants': 2,
# 'app_sequence': ['ultimatum', 'payment_info'],
# 'use_strategy_method': False,
# },
# {
# 'name': 'vickrey_auction',
# 'display_name': "Vickrey Auction",
# 'num_demo_participants': 3,
# 'app_sequence': ['vickrey_auction', 'payment_info'],
# },
# {
# 'name': 'volunteer_dilemma',
# 'display_name': "Volunteer's Dilemma",
# 'num_demo_participants': 3,
# 'app_sequence': ['volunteer_dilemma', 'payment_info'],
# },
# {
# 'name': 'cournot',
# 'display_name': "Cournot Competition",
# 'num_demo_participants': 2,
# 'app_sequence': [
###         'cournot', 'payment_info'
# ],
# },
# {
# 'name': 'principal_agent',
# 'display_name': "Principal Agent",
# 'num_demo_participants': 2,
# 'app_sequence': ['principal_agent', 'payment_info'],
# },
# {
# 'name': 'dictator',
# 'display_name': "Dictator Game",
# 'num_demo_participants': 2,
# 'app_sequence': ['dictator', 'payment_info'],
# },
# {
# 'name': 'matching_pennies',
# 'display_name': "Matching Pennies",
# 'num_demo_participants': 2,
# 'app_sequence': [
# 'matching_pennies',
# ],
# },
# {
# 'name': 'traveler_dilemma',
# 'display_name': "Traveler's Dilemma",
# 'num_demo_participants': 2,
# 'app_sequence': ['traveler_dilemma', 'payment_info'],
# },
# {
# 'name': 'bargaining',
# 'display_name': "Bargaining Game",
# 'num_demo_participants': 2,
# 'app_sequence': ['bargaining', 'payment_info'],
# },
# {
# 'name': 'common_value_auction',
# 'display_name': "Common Value Auction",
# 'num_demo_participants': 3,
# 'app_sequence': ['common_value_auction', 'payment_info'],
# },
# {
# 'name': 'bertrand',
# 'display_name': "Bertrand Competition",
# 'num_demo_participants': 2,
# 'app_sequence': [
###         'bertrand', 'payment_info'
# ],
# },
# {
# 'name': 'real_effort',
# 'display_name': "Real-effort transcription task",
# 'num_demo_participants': 1,
# 'app_sequence': [
# 'real_effort',
# ],
# },
# {
# 'name': 'lemon_market',
# 'display_name': "Lemon Market Game",
# 'num_demo_participants': 3,
# 'app_sequence': [
###         'lemon_market', 'payment_info'
# ],
# },
# {
# 'name': 'public_goods_simple',
# 'display_name': "Public Goods (simple version from tutorial)",
# 'num_demo_participants': 3,
# 'app_sequence': ['public_goods_simple', 'payment_info'],
# },
# {
# 'name': 'trust_simple',
# 'display_name': "Trust Game (simple version from tutorial)",
# 'num_demo_participants': 2,
# 'app_sequence': ['trust_simple'],
# },
