import bge
import time
import socket
import _thread
import queue

# UDP setup
# "127.0.0.1" does not work
UDP_IP = "192.168.0.255"
UDP_PORT = 23000
# A msg is typically 40 bytes long, so this is just for safety
BYTE_LENGTH = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

finished = False
q = queue.Queue()

"""
https://docs.python.org/2/howto/sockets.html
https://docs.python.org/3/library/queue.html
"""

def fetch_data():
    global q
    print("-fetch data-")

    while not finished:
        try:
            # buffer size must be a power of 2
            data, addr = sock.recvfrom(BYTE_LENGTH)
            print("Rec msg:", data)
            print("Clientadresse:", addr)
            q.put(data)

        except:
            pass

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
