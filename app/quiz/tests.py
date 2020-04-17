from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants



class PlayerBot(Bot):
    def dump_html(self,_html):
        if Constants.TESTS_EXPORT_HTML:
            print("\n\n\n")
            print("<article>")
            print(_html)
            print("</article>")
            print("\n\n\n")
            print("<hr />\n\n\n")


    def play_round(self):
        if self.round_number == 1:
            self.dump_html(self.html)
            yield (pages.Intro1)
            self.dump_html(self.html)
            yield (pages.Intro2)
            self.dump_html(self.html)
            yield (pages.Intro3)
            self.dump_html(self.html)
            yield (pages.Intro4)
            self.dump_html(self.html)
            yield (pages.Intro5)
            self.dump_html(self.html)
            yield (pages.Intro6)
            self.dump_html(self.html)
            yield (pages.Intro7)
            self.dump_html(self.html)
            yield (pages.Examples)
            self.dump_html(self.html)
            yield (pages.Example1)
            self.dump_html(self.html)
            yield (pages.Example2)
            self.dump_html(self.html)
            yield (pages.Example3)
            self.dump_html(self.html)
            yield (pages.PracticeIntro)
            self.dump_html(self.html)
            yield (pages.PracticeGame1, {'practice_contrib1': c(10)})
            self.dump_html(self.html)
            yield (pages.PracticeResults1)
            self.dump_html(self.html)
            yield (pages.PracticeGame2, {'practice_contrib2': c(10)})
            self.dump_html(self.html)
            yield (pages.PracticeResults2)
            self.dump_html(self.html)
            yield (pages.Quiz)
            self.dump_html(self.html)
            yield (pages.Quiz1, {'q1': 1}) # 3
            self.dump_html(self.html)
            yield (pages.ReviewGameRules)
            self.dump_html(self.html)
            yield (pages.Quiz1, {'q1': 2})
            self.dump_html(self.html)
            yield (pages.Quiz2, {'q2': 1 }) #Constants.q2[0]["answer"] = true
            # yield (pages.ReviewGameRules)
            # yield (pages.Quiz2, {'q2': 0 })
            yield (pages.Quiz3, {
                'q3a': 1,
                'q3b': 0
            })
            self.dump_html(self.html)
            yield (pages.Quiz4, {
                'q4a': 2, # 2 Constants.q4[0]["answer"],
                'q4b': 1, # 1 Constants.q4[1]["answer"],
                'q4c': 2, # 2 Constants.q4[2]["answer"],
                'q4d': 2, # 2 Constants.q4[3]["answer"],
                'q4e': 1, # 1 Constants.q4[4]["answer"],
                'q4f': 2, # 2 Constants.q4[5]["answer"]
            })
            self.dump_html(self.html)
            yield (pages.GameIntro)
            self.dump_html(self.html)
