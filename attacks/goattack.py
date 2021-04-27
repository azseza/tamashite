

class HttpGoFood:
    """
    The golang httpFlood attack lunch
    """
    gofile = "httpflood.so"
    lib_name = "mainer"

    def __init__(self):
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
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lib = cdll.LoadLibrary(os.path.join(dir_path, "httpflood.so"))
                #lib = cdll.LoadLibrary('./httpflood.so')
                print("here")
                lib(self.target, self.numberOfBots)
            else:
                raise FileNotFoundError
        except BrokenGoFile:
            log("something went wrong with the Go interpreter", color="red")
        except FileNotFoundError:
            log("Did You make the project ? Go executable not found!", color="red")
        except NameError:
            log("Go object shared library not found, Did You make the project ? ", color="red")

