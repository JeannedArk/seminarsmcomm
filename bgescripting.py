import bge
import time
import socket
import _thread
import queue



# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 23000

# Die Konstante AF_INET steht für Adressfamilie Internet.
# Die Konstante SOCK_DGRAM steht für das UDP-Protokoll.
# Dies sind optionale Eingaben für eine Socket-Instanz.
# Voreingestellt ist AF_INET und als Protokoll SockStream, dies steht für
# ein TPC-socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
finished = False
q = queue.Queue()

"""
https://docs.python.org/3/library/asyncio-eventloop.html
https://docs.python.org/2/howto/sockets.html
https://docs.python.org/3/library/queue.html
"""

def fetch_data():
    global q
    print("-fetch data-")

    while not finished:
        try:
            print("fetch data while")
            # buffer size must be a power of 2
            data, addr = sock.recvfrom(1024)
            print("Rec msg:", data)
            print("Clientadresse:", addr)
            q.put(data)
            
        except:
            pass
            #print("socket timeout ")

def init():
    print("UDPSceneMakerCommunication init")
    bge.render.showMouse(True)
    _thread.start_new_thread(fetch_data, ())

#TODO naming
def keypressed():
    global finished
    print("key pressed")

    #kill thread
    finished = True
    #end game engine
    bge.logic.endGame()


def update():
    #print("update: ")
    global q
    #get data if there
    if not q.empty():
        data = q.get()
    #TODO do something with the data


def send(msg):
    print("Message:", msg)
    sock.sendto(msg, (UDP_IP, UDP_PORT))
