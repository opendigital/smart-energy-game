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
    name_in_url = 'training'
    num_rounds = 1
    players_per_group = None
    game_goal = 900
    game_players = 25
    game_rounds = 6
    game_tokens = 10
    quiz_max_attempts = 2
    reduction_goal = 60
    token_goal = 900
    token_value = .01
    carbon_per_token = 2.2

    page_titles = dict(
        intro1="Research Participant Consent Form",
        intro2="Outline",
        intro3="Introduction",
        intro4="Instruction: Game Structure and Incentives",
        intro5="Instruction: Gameplay",
        intro6="Instruction: Financial Outcomes",
        intro7="Instruction: Environmental Outcomes",
        examples="Examples",
        example1="Examples 1: Minimum Requirement to Meet the Goal",
        example2="Examples 2 and 3: Min and Max Conservation",
        example3="Examples 4 and 5: Only You vs. Everyone But You",
        practiceintro="Practice Rounds",
        practicegame1="Practice Rounds",
        practicegame2="Practice Rounds",
        practiceresults1="Practice Rounds",
        practiceresults2="Practice Rounds",
        quiz="Comprehension Quiz",
        quiz1="Comprehension Quiz 1/6",
        quiz2="Comprehension Quiz 2/6",
        quiz3="Comprehension Quiz 3/6",
        quiz4="Comprehension Quiz 4/6",
        quiz5="Comprehension Quiz 5/6",
        quiz6="Comprehension Quiz 6/6",
        reviewgamerules="Review Game Rules",
        gameintro="Energy Conservation Game",
    )

    true_false = [
        [1, "True"],
        [0, "False"],
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

    quiz_progress = [
        1,
        2,
        3,
        4,
    ]

    quiz_default_hint = 'Please proceed to review instructions. \
        You will then return to this question and have one \
        more opportunity to answer it.'


    q1 = [
        dict(
            label="How many tokens will each player need to contribute to the group conservation \
                 account in each round in order to meet the 60% group conservation goal?",
            answer=3,
            choices=[
              [1, "2 tokens"],
              [2, "3 tokens"],
              [3, "6 tokens"],
              [4, "10 tokens"],
            ],
            hint="To meet the 60% energy conservation goal, each player should contribute 6 energy \
                tokens each month to the group conservation account, resulting in 900 energy \
                tokens at the end of the game.",
        )
    ]

    q2 = [
        dict(
            label='For each energy token in the group conservation account $0.01 is contributed to \
                Carbonfund.org to reduce actual air pollution in the U.S.',
            answer=1,
            choices=true_false,
            hint='Each token in the group conservation account equals $0.01 dollars. The \
                dollar value of the group conservation account is contributed to Carbonfund.org.',
        )
    ]

    q3 = [
        dict(
            label="You will have greater earnings than others if you put all of your energy tokens in \
                your private account, while others contribute all of theirs to the group conservation account",
            answer=1,
            choices=true_false,
            hint="You will have greater earnings if you put all of your energy tokens in your \
                private account, while others contribute all of their tokens in the group conservation account, \
                because the group meets the goal and everybody is paid an equal share of the bonus. So, you will earn \
                $0.60 from your private account + $1.15 bonus = $1.75, while others will only earn the \
                $1.15 bonus.",
        ),
        dict(
            label='True or False: The group will maximize its earning if all players contribute 6 of their energy tokens to the group conservation account each month',
            answer=0,
            choices=true_false,
            hint="The group gets the maximum financial payment if all players contribute \
                all 10 tokens in the conservation account in each month (25 players \
                &times; 10 tokens &times; 6 months &times; $.01 = $15). Every player then gets an equal \
                share of the maximum bonus possible, which is double the value of the \
                tokens in the conservation account (2 &times; $15 &divide; 25 players = $1.20).",
        )
    ]

    q4 = [
        dict(
            label="My payout from my private account is",
            answer=2,
            choices=[
                [1, "$0.00"],
                [2, "$0.30"],
                [3, "$3.00"],
            ],
            hint="The correct answer is $0.30. You are paid $0.01 for each of the 30 energy tokens left in your private account.",
        ),
        dict(
            label="My bonus payout from the group conservation account is",
            answer=1,
            choices=[
                [1, "$0.36"],
                [2, "$0.72"],
                [3, "$0.90"],
            ],
            hint="The correct answer is $0.72. The 900 energy tokens meets the conservation goal, so the $9 is doubled to \
                $18 and distributed equally to all 25 players, resulting in a $0.72 bonus pay.",
        ),
        dict(
            label="My total payout is (private + group conservation bonus)",
            answer=2,
            choices=[
                [1, "$0.36"],
                [2, "$0.66"],
                [3, "$1.02"],
            ],
            hint="The correct answer is $1.02. Add the energy token value in your \
                private account ($0.30) and the bonus ($0.72) to get your final pay of $1.02.",
        ),
        dict(
            label="My payout from my private account is",
            answer=2,
            choices=[
                [1, "$0.00"],
                [2, "$0.30"],
                [3, "$3.00"],
            ],
            hint="The correct answer is $0.30. You are paid $0.01 for each of the 30 energy tokens \
                left in your private account, even if the group does not meet the conservation goal of 900 tokens",
        ),
        dict(
            label="My payout from the group conservation account is",
            answer=1,
            choices=[
                [1, "$0.00"],
                [2, "$0.34"],
                [3, "$0.68"],
            ],
            hint="The correct answer is $0.00. The 850 energy tokens do not meet the \
                group conservation goal of 900 energy tokens, so no conservation bonus is paid. ",
        ),
        dict(
            label="Total payout is (private + group conservation bonus)",
            answer=2,
            choices=[
                [1, "$0.30"],
                [2, "$0.64"],
                [3, "$0.98"]
            ],
            hint=") The correct answer is $0.30. Add the energy token values in your private account \
                ($0.30) and the bonus from the group conservation account ($0.00) to get your final pay of $0.30.",
        )
    ]
