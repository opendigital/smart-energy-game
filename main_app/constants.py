from otree.api import (
    BaseConstants,
    Currency as c,
)


class Constants(BaseConstants):
    """model docstring"""

    def __init__(self):
        self.values = ''


    multiplier = 2
    name_in_url = 'energy-game'
    players_per_group = None
    # players_without_me = players_per_group - 1
    reduction_goal = 60
    num_actual_rounds = 6
    game_rounds = 6
    game_players = 25
    num_rounds = num_actual_rounds + 1
    endowment = c(100)
    group_goal = c(900)
    no_bonus = c(0)


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


    quiz_hint = [
        'To meet the 60% energy conservation goal, each player should contribute 6 energy tokens each month to the group conservation account, resulting in 900 energy tokens at the end of the game.',
        'Each token in the group conservation account equals $0.01 dollars. The dollar value of the group conservation account is contributed to Carbonfund.org.',
        'You will have greater earnings if you put all of your energy tokens in your private account, while others \
            contribute all of their tokens in the group conservation account, because the group \
            meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
            $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
            $1.15 bonus. (If wrong take back to 3rd page of EXAMPLES: full table',
        'The group gets the maximum financial payment if all players contribute all 10 tokens in the \
            conservation account in each month (25 players x 10 tokens x 6 months x $.01 = \
            $15). Every player then gets an equal share of the maximum bonus possible, which is \
            double the value of the tokens in the conservation account (2 x $15 / 25 players = \
            $1.20).',
        "$1.00",
        "$18.18",
        "$19.18",
        "$1.00",
        "$0.00",
        "$1.00",
    ]



    quiz_default_hint = 'Please proceed to Review Instructions. \
        You will then return to this question and have one \
        more opportunity to answer it'


    q1_labels = [
        quiz_default_hint,
        'On average, how many tokens will each player need \
        to invest into the group conservation account in each round in order \
        to meet the 60% group conservation goal?'
    ]

    q1_choices = [
        "2 tokens",
        "3 tokens",
        "6 tokens",
        "11 tokens"
    ]

    q1_answers = [
        '6 tokens'
    ]

    q1_hints = [
        'To meet the 60% energy conservation goal, each player should contribute 6 energy \
            tokens each month to the group conservation account, resulting in 900 energy \
            tokens at the end of the game.',
    ]


    quiz_1_label = 'For each energy token in the group conservation \
        account $0.01 is contributed to Carbonfund.org to reduce actual \
        air pollution in the real world?'
    ]


    quiz_2_label = 'For each energy token in the group conservation \
        account $0.01 is contributed to Carbonfund.org to reduce actual \
        air pollution in the real world?'

    quiz_3a_label = 'You will have greater benefits than others if you \
        keep all of your energy tokens for yourself, while others invest \
        all of theirs to the group conservation account.'
    quiz_3b_label = 'The group will maximize its benefits if all players \
        invest, on average, 6 of their energy tokens to the \
        group conservation account.'



    quiz_4a1_label = 'My payout from my personal account is'
    quiz_4a2_label = 'My payout from the group conservation account is'
    quiz_4a3_label = 'Total payou"$1.t is (personal plus conservation)'
    quiz_4b1_label = 'My payout from my personal account is'
    quiz_4b2_label = 'My payout from the group conservation account is'
    quiz_4b3_label = 'Total payout is (personal plus conservation)'


    answers = [
        "6 tokens",
        "True",
        "True",
        "True",
        "$1.00",
        "$18.18",
        "$19.18",
        "$1.00",
        "$0.00",
        "$1.00"
    ]


    survey_1_q1 = 'What were you trying to do in the experiment (in other words: what were your goals or objectives)?'
    survey_1_q2 = 'Did you achieve your objectives?'
    survey_1_q3 = 'What information guided your contributions throughout the game?'
    survey_1_q4 = 'What were the other members of your group trying to do (what were their objectives)?'
    survey_1_q5 = 'What was the scope of this experiment (in other words, what were the experimenters trying to discover)?'
    survey_1_qb1 = 'This experiment requires a great concentration effort.'
    survey_1_qb2 = 'The rules of the game were explained clearly and were understandable.'
    survey_1_qb3 = 'One must try to work together with others to have everyone end up with more money.'
    survey_1_qb4 = 'The group goal did not matter because any conservation had an impact (it was donated to remove air pollution in the US).'
    survey_1_qb5 = 'Everyone\'s earnings depend on the decisions of all members of the group.'
    survey_1_qc1 = 'Your past contributions'
    survey_1_qc2 = 'Other\'s total contributions to the group conservation account'
    survey_1_qc3 = 'Total contributions to date (yours and others\' together) to the group conservation account'
    survey_1_qc4 = 'Percentage of group goal met'
    survey_1_qc5 = 'The environmental benefits of conservation (the donation to remove air pollution in the US)'
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
        'People in the United States',
    ]

    survey_4_items = [
        'What is your year of birth?',
        'What is your gender?',
        'What term best describes your racial identity?',
        'What is your economic status?',
        'How many multi-player game experiments like the one you just played have you participated in before this one?',
        'Are your responses reliable enough for us to include them in our academic research that will have real implications on energy and housing community policy making?',
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


    range_5_important = [
        [1, 'Not Important'],
        [2, 'A Little Important'],
        [3, 'Medium Important'],
        [4, 'Moderately Imporant'],
        [5, 'Very Important']
    ]

    choice_demographics_gender = [
        'Male',
        'Female',
        'Other'
    ]

    choices_demographics_ethnicity = [
        'American Indian/Alaska Native',
        'Asian',
        'Black or African-American',
        'Native Hawaiian/Pacific Islander',
        'White',
        'Other',
    ]

    choices_demographics_employment = [
        'Full time employed',
        'Full time student',
        'Part time employed',
        'Part time student',
        'Other'
    ]

    choices_demographics_experience = [
        'None',
        '1-2 previous',
        '3-5 previous',
        'More than 5 previous'
    ]

    choices_demographics_political = [
        'Democrat',
        'Republican',
        'Independent',
        'Other'
    ]
