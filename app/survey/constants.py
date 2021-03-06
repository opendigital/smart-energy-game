from otree.api import (
    BaseConstants,
)


class Constants(BaseConstants):
    def __init__(self):
        self.values = ''

    template_config = dict(
        debug_vars=False,
        debug_jsvars=False
    )

    TESTS_EXPORT_HTML = True
    num_rounds = 1
    name_in_url = 'post-game'
    players_per_group = None
    game_rounds = 1

    page_titles = dict(
        PostSurvey1="Post-Game Survey 1/4",
        PostSurvey2="Post-Game Survey 2/4",
        PostSurvey3="Post-Game Survey 3/4",
        PostSurvey4="Post-Game Survey 4/4",
    )

    true_false = [
        [1, "True" ],
        [0, "False" ],
    ]

    MONTHS = [
        'JANUARY',
        'FEBRUARY',
        'MARCH',
        'APRIL',
        'MAY',
        'JUNE',
        'JULY',
        'AUGUST',
        'SEPTEMBER',
        'OCTOBER',
        'NOVEMBER',
        'DECEMBER'
    ]

    survey_1a_items = [
        "What were you trying to do in the game (in other words: what were your goals or objectives)?",
        "Did you achieve your objectives?",
        "What information guided your decisions throughout the game?",
        "What were the other members of your group trying to do (what were their objectives)?",
        "What was the scope of this experiment (in other words, what were the experimenters trying to discover)?",
    ]

    survey_1b_items = [
        "This experiment requires a lot of concentration.",
        "The rules of the game were explained clearly.",
        "In this experiment one must try to work together with others to have everyone end up with more money.",
        "In this experiment, the air pollution impact was more important to me than the financial incentive for \
            meeting the group conservation goal (i.e. the bonus).",
        "In this experiment, everyone\'s earnings depend on the decisions of all members of the group.",
    ]

    survey_1c_items = [
        "My past contributions to the group conservation account.",
        "Others' average contributions to the group conservation account.",
        "Total contributions to the group conservation account from all 25 players.",
        "Cumulative percentage of the group goal achieved.",
        "The environmental benefits of conservation (the donation to remove air pollution).",
    ]

    survey_2_items = [
        'I like to help other people',
        'I like to share my ideas and materials with others',
        'People learn lots of important things from each other',
        'I work to get better than others',
        'I like to be the best at what I do',
        'I like the challenge of seeing who is best',
        'I don\'t like working with others',
        'It bothers me when I have to work with others',
        'I work better when I do it all myself',
    ]

    survey_3_items = [
        'Plants',
        'Marine life',
        'Birds',
        'Animals',
        'My prosperity',
        'My lifestyle',
        'My health',
        'My future',
        'People in my community',
        'The human race',
        'Children',
    ]

    survey_4_items = [
        'What is your year of birth?',
        'What is your gender?',
        'What term best describes your racial identity?',
        'What is your economic status?',
        'How many multi-player game experiments like the one you just played have you \
            participated in before this one?',
        'Are your responses reliable enough for us to include them in our academic \
            research that will have real implications on energy and housing community policy making?',
        'Which political party do you most identify with?',
        'How many years have you lived in the US?',
    ]

    range_influence = [
        [1, '1 - Not At All Influential'],
        [2, '2 - A Little Influential'],
        [3, '3 - Moderately Influential'],
        [4, '4 - Very Influential'],
    ]

    range_concerned = [
        [0, ''],
        [1, ''],
        [2, ''],
        [3, ''],
        [4, ''],
    ]

    range_5 = [1, 2, 3, 4, 5]

    range_5_truth = [
        [1, 'Definitely false'],
        [2, 'Probably false'],
        [3, 'Not sure'],
        [4, 'Definitely true'],
        [5, 'Probably true']
    ]

    range_5_important = [
        [1, 'Not Important'],
        [2, 'A Little Important'],
        [3, 'Medium Important'],
        [4, 'Moderately Imporant'],
        [5, 'Very Important']
    ]

    choice_demographics_gender = [
        [1, 'Male' ],
        [2, 'Female' ],
        [3, 'Other' ],
    ]

    choices_demographics_ethnicity = [
        [1, 'American Indian/Alaska Native'],
        [2, 'Asian'],
        [3, 'Black or African-American'],
        [4, 'Native Hawaiian/Pacific Islander'],
        [5, 'White'],
        [6, 'Other'],
    ]

    choices_demographics_employment = [
        [1, 'Full time employed'],
        [2, 'Full time student'],
        [3, 'Part time employed'],
        [4, 'Part time student'],
        [5, 'Retired'],
        [6, 'Other'],
    ]

    choices_demographics_experience = [
        [1, 'None'],
        [2, '1-2 previous'],
        [3, '3-5 previous'],
        [4, 'More than 5 previous'],
    ]

    choices_demographics_political = [
        [1, 'Democrat'],
        [2, 'Republican'],
        [3, 'Independent'],
        [4, 'Other'],
    ]
