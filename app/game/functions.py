
DIVIDER_LINE_MAJOR = "========================================================="
DIVIDER_LINE_MINOR = "--------------------------------------------------------"
LINE_BREAK = "\n\n"

class Functions():
    def __init__(self):
        self.values = ''

    @staticmethod
    def print_round_results(round_number, data):
        game_total_contrib_label = "game_total_contrib                   \t"
        player_withheld_label = "player_withheld              \t"
        player_contributed_label = "player_contributed           \t"
        player_total_witheld_label = "player_total_witheld         \t"
        player_total_contrib_label = "player_total_contrib     \t"
        group_round_contributions_label = "group_round_contributions    \t"
        group_round_withholdings_label = "group_round_withholdings     \t"
        group_round_contrib_total_label = "group_round_contrib_total         \t"
        group_round_witheld_total_label = "group_round_witheld_total         \t"
        player_past_contributions_label = "player_past_contributions    \t"
        player_past_witholdings_label = "player_past_witholdings      \t"
        group_round_contrib_label = "group_round_contrib        \t"

        print(DIVIDER_LINE_MAJOR)
        print('ROUND NUMBER', round_number)
        print(game_total_contrib_label, data["game_total_contrib"])

        print(DIVIDER_LINE_MAJOR)
        print(player_withheld_label, data["player_withheld"])
        print(player_contributed_label, data["player_contributed"])

        print(DIVIDER_LINE_MINOR)
        print(player_total_witheld_label, data["player_total_witheld"])
        print(player_total_contrib_label, data["player_total_contrib"])

        print(DIVIDER_LINE_MINOR)
        print(group_round_contributions_label, data["group_round_contributions"])
        print(group_round_withholdings_label, data["group_round_withholdings"])

        print(DIVIDER_LINE_MINOR)
        print(group_round_contrib_total_label, data["group_round_contrib_total"])
        print(group_round_witheld_total_label, data["group_round_witheld_total"])
        print(player_past_contributions_label, data["player_past_contributions"])
        print(player_past_witholdings_label, data["player_past_witholdings"])
        print(group_round_contrib_label, data["group_round_contrib"])

        print(LINE_BREAK)

    @staticmethod
    def print_bot_round_result(round_conributions, diff, trend):
        round_str = ''
        diff_str = ''
        for val in round_conributions:
            round_str += str(val).rjust(4, ' ')

        round_str += "|count: " + str(len(round_conributions))
        round_str += "|sum: " + str(sum(round_conributions))
        round_str += "|avg: " + str(float(sum(round_conributions) / len(round_conributions)))
        round_str += "|trend: " + trend
        print(round_str)
        for val in diff:
            diff_str += str(val).rjust(4, ' ')
        print(diff_str)


    @staticmethod
    def get_contribution_trend(p_contrib, p_contrib_prev, bot_contrib, bot_contrib_prev):
        contributions_total = p_contrib + sum(bot_contrib)
        contributions_total_prev = p_contrib_prev + sum(bot_contrib_prev)

        if contributions_total > contributions_total_prev:
            return "up"
        elif contributions_total < contributions_total_prev:
            return "down"
        else:
            return "stable"


    @staticmethod
    def print_game_result_table(data):
        print('=================================================================================================================')
        print('    #  |  P  | BOTS                                                                    |  t   Δt   x̄    Δx̄       ')
        print('-----------------------------------------------------------------------------------------------------------------')

        game_total_contrib = 0
        round_num = 0

        contrib = data["player_contributions"].copy()
        for bot_round in data["bot_contributions"]:
            round_num += 1
            player_round = (contrib.pop(0))
            player_round_str = "[ " + str(player_round).rjust(2, ' ')

            if round_num > 1:
                round_total_prev = bot_round_total
                bot_round_total = sum(bot_round) + int(player_round)
                diff_total = int(bot_round_total) - int(round_total_prev)

                if (diff_total > 0):
                    diff_total_str = "(+" + str(diff_total) + ")"
                elif (diff_total < 0):
                    diff_total_str = "(" + str(diff_total)+ ")"
                else:
                    diff_total_str = ""
            else:
                bot_round_total = sum(bot_round) + int(player_round)
                diff_total_str = ""


            if round_num > 1:
                round_avg_prev = round_avg
                round_avg = float(bot_round_total / (len(bot_round) + 1))
                diff_avg = round(float(round_avg) - float(round_avg_prev), 4)

                if (diff_avg > 0):
                    diff_avg_str = "(+" + str(diff_avg).ljust(4, '0') + ")"
                elif (diff_avg < 0):
                    diff_avg_str = "(" + str(diff_avg).ljust(4, '0')+ ")"
                else:
                    diff_avg_str = "    "
            else:
                diff_avg_str = "    "
                round_avg = float(bot_round_total / (len(bot_round) + 1))

            round_avg_str = str(round_avg).ljust(4, '0')
            game_total_contrib += bot_round_total
            bot_round_str = ""
            for bot_val in bot_round:
                bot_round_str += str(bot_val).rjust(3, ' ')

            print(
                "|| ("+ str(round_num) + ")",
                player_round_str, "|",
                bot_round_str.lstrip(), "]", '|',
                str(bot_round_total),
                str(diff_total_str).rjust(4, ' '),
                str(round_avg_str),
                str(diff_avg_str).rjust(7, ' '), '||',
                str(game_total_contrib)
            )

        print('-----------------------------------------------------------------------------------------------------------------')
        print('GAME TOTAL:                \t',   data["game_contributions_total"])
        print('_________________________________________________________')
        print('PLAYER:')
        print('  player_contributions       \t', data["player_contributions"])
        print('  total contrib              \t', data["player_total_contributed"])
        print('  total witheld              \t', data["player_total_witheld"])
        print('  total_payoff               \t', data["player_total_payoff"])
        print('  quiz_bonus                 \t', data["player_quiz_bonus"])
        print('  game_bonus                 \t', data["player_game_bonus"])
        print('  payoff                     \t', data["player_payoff"])
        print('  payoff_plus_partip_fee     \t', data["player_payoff_plus_partip_fee"])

        print('\n\n')
        print(data["player_vars"])
