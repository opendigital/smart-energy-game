from datetime import date
import json
import inspect
from .constants import Constants

class Utils():
    # def __init__(self):

    def get_date():
        today = date.today()
        return today

    def get_month(index):
        today = date.today()
        start_month = today.month - 1
        return Constants.MONTHS[(12 + start_month + index) % 12]


    def print_var(somevar, title=""):
        if title:
            print(title)

        variables = [i for i in dir(somevar) if not inspect.ismethod(i)]
        print(json.dumps(somevar, separators=(". ", ":"), indent=4))


    def dump(obj, title=''):
        if title is not "":
            print("")
            print(title)

        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))


    def dump_obj(obj, title=""):
        if title is not "":
            print("")
            print(title)

        vars = obj.__dict__.keys()
        for v in vars:
            print(v, '\t\t', getattr(obj, v))


    def isset(arg):
        print("testing argument", arg)
        try:
            arg
        except NameError:
            arg = None
            print("except NameError", arg)

        if arg is None:
            print("arg is None", arg)
            return False
        else:
            print("returning argument", arg)
            return True
