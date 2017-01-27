import bge
import time
import socket
import _thread
import queue
import json

class ActionActivity(object):
    def __init__(self, atype, nameaction, object, name):
        self.atype = atype
        self.nameaction = nameaction
        self.object = object
        self.name = name

    def __str__(self):
        return "ActionActivity(object: " + self.object + " name: " + self.name + ")"

class SpeechActivity(object):
    def __init__(self, atype, object, text):
        self.atype = atype
        self.object = object
        self.text = text

    def __str__(self):
        return "SpeechActivity(object: " + self.object + " text: " + self.text + ")"

# UDP setup
# "127.0.0.1" does not work
UDP_IP = "192.168.0.255"
UDP_PORT = 23000
# A msg is typically 40 bytes long, so this is just for safety
BYTE_LENGTH = 256

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

finished = False
q = queue.Queue()

"""
https://docs.python.org/2/howto/sockets.html
https://docs.python.org/3/library/queue.html
"""

def message_to_json(msg):
    j = json.loads(msg)
    if "\"atype\": \"action\"" in msg:
        return ActionActivity(**j)
    elif "\"atype\": \"speech\"" in msg:
        return SpeechActivity(**j)
    else:
        print("Not a known type")
        raise Exception("Not a known type")

def fetch_data():
    global q
    print("-fetch data-")

    while not finished:
        try:
            data, addr = sock.recvfrom(BYTE_LENGTH)
            activity = message_to_json(data.decode())
            #print("act: " + str(activity))
            q.put(activity)
        except Exception as msg:
            print(msg)

def init():
    print("UDPSceneMakerCommunication init")
    bge.render.showMouse(True)
    _thread.start_new_thread(fetch_data, ())

#TODO naming
def keypressed():
    global finished
    print("key pressed")

    # Kill thread
    finished = True
    # End socket communication
    sock.close()
    # End game engine
    bge.logic.endGame()


def update():
    global q
    if not q.empty():
        data = q.get()
        print("update: " + str(data))
