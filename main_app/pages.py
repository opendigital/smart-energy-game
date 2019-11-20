from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from main_app import models


class WaitingRoom(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."
    #group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1


class ConsentForm(Page):
    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Consent'}


class GameFraming(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameStructure1(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction1 == 0) or (self.round_number == 2 and self.player.repeatQuiz1)

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction1 += 1


class GameStructure2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameOutcomes1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Introduction'}


class GameOutcomes2(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction2 == 0) or (
                self.round_number == 2 and self.player.repeatQuiz2)

    def vars_for_template(self):
        return {'progress': 'Introduction'}

    def before_next_page(self):
        self.player.timesInstruction2 += 1


class ExamplesTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Examples'}


class ExamplesOne(Page):
    def is_displayed(self):
        return(self.round_number == 1 and self.player.timesInstruction4 == 0) or (
                self.round_number == 2 and self.player.repeatQuiz4)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction4 += 1


class ExamplesTwo(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3a == 0) or (
                self.round_number == 2 and self.player.repeatQuiz3a)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction3a += 1


class ExamplesThree(Page):
    def is_displayed(self):
        return (self.round_number == 1 and self.player.timesInstruction3b == 0) or (
                self.round_number == 2 and self.player.repeatQuiz3b)

    def vars_for_template(self):
        return {'progress': 'Examples'}

    def before_next_page(self):
        self.player.timesInstruction3b += 1


class PracticeTransition(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'progress': 'Practice'}


class PracticeGame(Page):
    form_model = 'player'
    form_fields = ['practice_contribution']

    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds / 2,
                'progress': 'Practice'}

    def before_next_page(self):
        self.player.practice_private_contribution = c(10) - self.player.practice_contribution
        self.player.random_others_contribution = c(0)
        for i in range(0, Constants.players_per_group):
            self.player.random_others_contribution += c(random.randint(0,11))
        self.player.group_random_total_contribution = self.player.practice_contribution + self.player.random_others_contribution


class PracticeResults(Page):
    def is_displayed(self):
        return self.round_number <= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 1) % 12],
                'current_round': self.round_number % 12,
                'is_trial': self.round_number <= Constants.num_rounds/2,
                'progress': 'Practice'}


class QuizTransition(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return {'progress': 'Quiz'}


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['Q1']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[0],
                'xINST':self.player.timesInstruction1,
                'REP?':self.player.repeatQuiz1}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction1 <= 1 and not self.player.is_equilibrium_tokens_correct()

    def Q1_choices(self):
        choices = ["2 tokens", "3 tokens", "6 tokens", "10 tokens"]
        #random.shuffle(choices)#Fix for randomness
        return choices

    def before_next_page(self):
        if self.player.is_equilibrium_tokens_correct():
            self.player.repeatQuiz1 = False
        else:
            self.player.repeatQuiz1 = True


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['Q2']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': Constants.answers[1]}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction1 <= 1 and not self.player.is_donation_correct()

    def Q2_choices(self):
        choices = ["True","False"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.is_donation_correct():
            self.player.repeatQuiz2 = False
        else:
            self.player.repeatQuiz2 = True


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['Q3a', 'Q3b']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'correct_answer': 'True',
                'correct_answer2': 'True',
                }

    def is_displayed(self):
        return self.round_number == 2 and (self.player.timesInstruction3a <= 1 or self.player.timesInstruction3b <= 1) and not self.player.is_both_Examples_right()

    def Q3a_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def Q3b_choices(self):
        choices = ["True", "False"]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        if self.player.is_both_Examples_right():
            self.player.repeatQuiz3a = False
            self.player.repeatQuiz3b = False
        else:
            if self.player.is_max_individual_correct():
                self.player.repeatQuiz3a = False
            else:
                self.player.repeatQuiz3a = True

            if self.player.is_max_group_correct():
                self.player.repeatQuiz3b = False
            else:
                self.player.repeatQuiz3b = True


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['Q4a1','Q4a2','Q4a3',
                   'Q4b1','Q4b2','Q4b3']

    def vars_for_template(self):
        return {'progress': 'Quiz',
                'xINSTRUCTIONS':self.player.timesInstruction4,
                'correct_answer':'$1.00','correct_answer2':'$18.18','correct_answer3':'$19.18',
                'correct_answer4':'$1.00','correct_answer5':'$0.00','correct_answer6':'$1.00'}

    def is_displayed(self):
        return self.round_number == 2 and self.player.timesInstruction4 <= 1 and not self.player.is_all_values_right()

    def before_next_page(self):
        if self.player.is_all_values_right():
            self.player.repeatQuiz4 = False
        else:
            self.player.repeatQuiz4 = True


class RealGameTransition(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return {'progress': 'Game'}

"""
class RealGameTransition(Page):
    form_model = 'player'
    form_fields = ['tokens_question']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

    def is_displayed(self):
        return self.player.round_number == (Constants.num_rounds/2) or self.player.round_number == Constants.num_rounds

    def tokens_question_error_message(self, value):
        if not (0 <= value <= 7.20):
            return 'The value must be between 0 and 7.20'
        elif (value / 10) > 0.72:
            return 'Round the value up to two decimals'

    def before_next_page(self):
        self.player.is_tokens_question_correct()


class Quiz6(Page):
    form_model = 'player'
    form_fields = ['expected_contribution', 'expected_individual']

    def vars_for_template(self):
        return {'progress': 'Quiz'}

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds/2

    def error_message(self, values):
        if values["expected_contribution"] + values["expected_individual"] != 120:
            return 'The numbers must add up to 120'

    def before_next_page(self):
        self.player.check_answers()
"""


class Survey(Page):
    form_model = 'player'
    form_fields = ['contribution','private_contribution']

    def is_displayed(self):
        return self.round_number >= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class ResultsWaitPage(WaitPage):
    title_text = "Waiting Room"
    body_text = "Please wait until the other participants are ready."

    # models.Player.bot_contributions = [[10 for x in round_] for round_ in models.Player.bot_contributions]
    # print(models.Player.bot_contributions)

    def is_displayed(self):
        return self.round_number >= 2

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.set_bots()
        # self.models.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
        # print(self.models.group.bot_contributions)
        
        

    
    # def before_next_page(self):
    #     self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
    #     print("test")



class Results(Page):
    def is_displayed(self):
        return self.round_number >= 2

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}
    
    # def before_next_page(self):
    #     self.player.bot_contributions = [[10 for x in round_] for round_ in self.player.bot_contributions]
    #     print("test")


class Congrats(Page):
    # Displayed only in the last round
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game',
                'lbs': str(self.group.all_rounds_contribution()/10*22).split(" ")[0] + " lbs",
                'amount': c(self.group.all_rounds_contribution()).to_real_world_currency(self.session)}

class FinalResults(Page):
    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game',
                'goal_meet': Constants.group_goal <= self.group.all_rounds_contribution(),
                'carbonfund': self.group.all_rounds_contribution_in_dollars(),
                'quiz': c(self.player.how_many_good_answers()).to_real_world_currency(self.session)}

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def before_next_page(self):
        self.group.pay_carbonfund()
        self.group.pay_quizzes()


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['I_like_to_help_other_people',
                   'I_like_to_share_my_ideas_and_materials_with_others',
                   'I_like_to_cooperate_with_others',
                   'I_can_learn_important_things_from_others',
                   'I_try_to_share_my_ideas_and_resources_with_others',
                   'People_learn_lots_of_important_things_from_each_other',
                   'It_is_a_good_idea_for_people_to_help_each_other',
                   'I_like_to_do_better_work_than_others',
                   'I_work_to_get_better_than_others',
                   'I_like_to_be_the_best_at_what_I_do',
                   'I_dont_like_to_be_second',
                   'I_like_to_compete_with_other_students',
                   'I_am_happiest_when_I_am_competing_with_others',
                   'I_like_the_challenge_of_seeing_who_is_best',
                   'Competing_with_others_is_a_good_way_to_work',
                   'I_dont_like_working_with_others',
                   'I_like_to_work_with_others_reverse',
                   'It_bothers_me_when_I_have_to_work_with_others',
                   'I_do_better_when_I_work_alone',
                   'I_like_work_better_when_I_do_it_all_myself',
                   'I_would_rather_work_along_than_with_others',
                   'Working_in_small_groups_is_better_than_working_alone']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Survey',
                'forms': [
                    'I_like_to_help_other_people',
                   'I_like_to_share_my_ideas_and_materials_with_others',
                   'I_like_to_cooperate_with_others',
                   'I_can_learn_important_things_from_others',
                   'I_try_to_share_my_ideas_and_resources_with_others',
                   'People_learn_lots_of_important_things_from_each_other',
                   'It_is_a_good_idea_for_people_to_help_each_other',
                   'I_like_to_do_better_work_than_others',
                   'I_work_to_get_better_than_others',
                   'I_like_to_be_the_best_at_what_I_do',
                   'I_dont_like_to_be_second',
                   'I_like_to_compete_with_other_students',
                   'I_am_happiest_when_I_am_competing_with_others',
                   'I_like_the_challenge_of_seeing_who_is_best',
                   'Competing_with_others_is_a_good_way_to_work',
                   'I_dont_like_working_with_others',
                   'I_like_to_work_with_others_reverse',
                   'It_bothers_me_when_I_have_to_work_with_others',
                   'I_do_better_when_I_work_alone',
                   'I_like_work_better_when_I_do_it_all_myself',
                   'I_would_rather_work_along_than_with_others',
                   'Working_in_small_groups_is_better_than_working_alone'],
                'names': ['I like to help other people ','I like to share my ideas and materials with others ','I like to cooperate with others ','I can learn important things from others ','I try to share my ideas and resources with others when I think it will help them ','People learn lots of important things from each other ','It is a good idea for people to help each other  ','I like to do better work than others ','I work to get better than others ','I like to be the best at what I do ','I don’t like to be second ','I like to compete with other students to see who can do the best ','I am happiest when I am competing with others ','I like the challenge of seeing who is best ','Competing with others is a good way to work  ','I don’t like working with others ','I like to work with others (reverse) ','It bothers me when I have to work with others  ','I do better when I work alone ','I like work better when I do it all myself ','I would rather work along than with others','Working in small groups is better than working alone (reverse)'],
                'aux': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]}


class PostSurvey2(Page):
    form_model = 'player'
    form_fields = ['Plants','Marine_life','Birds','Animals','My_prosperity','My_lifestyle','My_health','My_future','People_in_my_community','The_human_race','Children','People_in_the_United_States']

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Survey',
                'forms': ['Plants','Marine_life','Birds','Animals','My_prosperity','My_lifestyle','My_health','My_future','People_in_my_community','The_human_race','Children','People_in_the_United_States'],
                'names': ['Plants','Marine life','Birds','Animals','My prosperity','My lifestyle','My health','My future','People in my community','The human race','Children','People in the United States'],
                'aux': [0,1,2,3,4,5,6,7,8,9,10,11]}


class PostSurvey3(Page):
    form_model = 'player'
    form_fields = ['birth', 'gender', 'ethnic_group', 'economic_status', 'previous_experiments', 'reliability','politic_party','years_in_us',
                    'early_conserve', 'middle_conserve', 'end_conserve', 'individual_conservation_feedback_rank', 'collective_conservation_feedback_rank',
                   'carbon_offset_feedback_rank', 'percent_goal_feedback_rank', 'total_contribution_feedback_rank']

    # OPEN_QUESTIONS in POST_SURVEY 3
    # early_conserve = models.StringField()
    # middle_conserve = models.StringField()
    # end_conserve = models.StringField()

    # individual_conservation_feedback_rank = models.IntegerField()
    # collective_conservation_feedback_rank = models.IntegerField()
    # carbon_offset_feedback_rank = models.IntegerField()
    # percent_goal_feedback_rank = models.IntegerField()
    # total_contribution_feedback_rank = models.IntegerField()

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'current_month': Constants.months[(self.round_number - 2) % 12],
                'current_round': self.round_number - 1,
                'progress': 'Game'}


class Debriefing(Page):
    def vars_for_template(self):
        return {'progress': 'End'}

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


page_sequence = [
    ConsentForm,
    # WaitingRoom,
    GameFraming,
    GameStructure1,
    GameStructure2,
    GameOutcomes1,
    GameOutcomes2,
    ExamplesTransition,
    ExamplesOne,
    ExamplesTwo,
    ExamplesThree,
    PracticeTransition,
    PracticeGame,
    PracticeResults,
    QuizTransition,
    Quiz1,
    GameStructure1,
    Quiz1,
    Quiz2,
    GameOutcomes2,
    Quiz2,
    Quiz3,
    ExamplesTwo,
    ExamplesThree,
    Quiz3,
    Quiz4,
    ExamplesOne,
    Quiz4,
    RealGameTransition,
    Survey,
    ResultsWaitPage,
    Results,
    Congrats,
    FinalResults,
    # PostSurvey,
    # PostSurvey2,
    PostSurvey3,
    Debriefing
]
