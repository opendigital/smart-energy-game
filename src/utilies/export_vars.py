from otree.models import Participant
import csv

ps = Participant.objects.all()
with open("output.csv", "a") as fp:
    wr = csv.writer(fp)
    for p in ps:
        wr.writerow([p.session.code, p.code, p.vars, ])
