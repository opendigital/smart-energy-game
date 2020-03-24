# RECIPROCATORS:
#
# Starting condition based on normal distribution,
# M and SD are defined based on simulation outcomes to meet a group goal;
# search with mean between
# M: 4 to 6 and
# SD: 0 to 1
#
# Probabilistic rule:
# OPTION 1: Reciprocity norm rule only
#           IF Total Contribution in Round 2>Total Contribution in Round 1:
#              Increase your contribution by 1 (Sum C1>SumC2, c3=c2+1)
#           IF Total  Contribution in Round 2<Total Contribution in Round 1:
#              Decrease contribution by 1 (Sum C1>SumC2, c3=c2-1)
#
# OPTION 2: Reciprocity norm rule plus Social Norm Rule
#           IF Total Contribution in Round 2>Total Contribution in Round 1
#           AND IF Individual contribution c2 < Social norm (mean) in Round 2
#               Increase your contribution by 1
#               Sum C1>SumC2 AND c2<meanC2
#                  c3=c2+1
#           IF Total Contribution in Round 2>Total Contribution in Round 1
#           AND IF Individual contribution c2 > Social norm (mean in Round 2)
#              No change
#
# OPTION 3 Reciprocity norm rule plus Social Norm Rule
#           IF Total Contribution in Round 2> Total Contribution in Round 1
#           AND IF Individual contribution c2 is at least 1 token below social norm (mean in Round 2)
#               Increase your contribution by 1
#              (Sum C1>SumC2 AND c2<=meanC2-1, c3=c2+1)
#           IF Total Contribution in Round 2 > Total Contribution in Round 1
#           AND IF Individual contribution c2 > Social norm (mean in Round 2)
#               No change

class SocialBot(object):
    """docstring for SocialBot."""

    def __init__(self, arg):
        super(SocialBot, self).__init__()
        self.arg = arg

    trend = "stable"

    # Cooperators:
    # Starting condition based on a normal distribution:
    #    M: 8 token per round,
    #    SD: 1 token per round
    #    No probabilistic rule
    cooperators = dict(
        start_avg=8,
        start_high=9,
        start_low=7,
        range=[10, 9, 8],
    )

    def cooperator_rules(self):
        # If TotalContribution in Round 2 > Total Contribution in Round 1:
        #      Increase your contribution by 1
        round_n1 =
        round_n2 =


    #  RECIPROCATORS:
    #  Starting condition based on normal distribution,
    #  M and SD are defined based on simulation outcomes to meet a group goal;
    #  search with mean between
    #  M: 4 to 6 and
    #  SD: 0 to 1
    #  Probabilistic rule:
    #     OPTION 1: Reciprocity norm rule only
    #           If Total Contribution in Round 2>Total Contribution in Round 1:
    #              Increase your contribution by 1 (Sum C1>SumC2, c3=c2+1)
    #           If Total  Contribution in Round 2<Total Contribution in Round 1:
    #              Decrease contribution by 1 (Sum C1>SumC2, c3=c2-1)
    reciprocators = dict(
        start_avg=5,
        start_high=6,
        start_low=4,
    )

    # FREE_RIDERS:
    #    M: 2 token per round,
    #    SD: 1 token per round
    freerider = dict(
        start_avg=2,
        start_high=3,
        start_low=1,
        range=[3,2,1]
    )
