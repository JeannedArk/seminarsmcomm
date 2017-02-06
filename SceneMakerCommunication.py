import bge
import bpy
import GameLogic
import time
import socket
import _thread
import queue
import json

from Activity import *

"""
SceneMakerCommunication

https://docs.python.org/2/howto/sockets.html
https://docs.python.org/3/library/queue.html
"""

# UDP setup
# "127.0.0.1" does not work
UDP_IP = "192.168.0.255"
UDP_PORT = 23000
# A msg is typically 40 bytes long, so this is just for safety
BYTE_LENGTH = 256

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    sock.bind((UDP_IP, UDP_PORT))
except:
    sock.bind(("10.9.23.255", UDP_PORT)) # at Uni

# finished will be set to True if the end function is called, then fetch_data
# will not be executed anymore and the thread closes
finished = False
# Thread safe FIFO queue for storing and getting the activities
q = queue.Queue()


def message_to_activity(msg):
    """Converts a given string in JSON format to SpeechActivity or ActionActivity"""

    print("message_to_activity: >" + msg + "<")
    j = json.loads(msg)
    if "\"atype\": \"action\"" in msg:
        return ActionActivity(**j)
    elif "\"atype\": \"speech\"" in msg:
        return SpeechActivity(**j)
    else:
        print("Not a known type")
        raise Exception("Not a known type")

def fetch_data():
    """Fetches the latest not yet fetched data from the socket and puts it into the queue"""
    global q

    while not finished:
        try:
            data, addr = sock.recvfrom(BYTE_LENGTH)
            activity = message_to_activity(data.decode())
            #print("act: " + str(activity))
            q.put(activity)
        except Exception as msg:
            print(msg)

def init():
    """Spawn a new thread for the fetching data"""

    print("SceneMakerCommunication init")
    bge.render.showMouse(True)
    _thread.start_new_thread(fetch_data, ())

def end():
    """Finish and close everything including the socket communication"""
    global finished

    print("SceneMakerCommunication end")

    # Kill thread
    finished = True
    # End socket communication
    sock.close()
    # End game engine
    bge.logic.endGame()

"""
def get_all_actions(obj):
  if obj.animation_data:
    if obj.animation_data.action:
      yield obj.animation_data.action
    for track in obj.animation_data.nla_tracks:
      for strip in track.strips:
        yield strip.action
"""

def execute(activity):
    """Execute the passed activity. It is either a SpeechActivity or ActionActivity

    Note: Executing the SpeechActivity is not yet implemented, but should be relatively easy
    if the connection with MaryTTS works.
    """
    print("execute: " + str(activity))
    #c = GameLogic.getCurrentController()
    #print(">" + activity.atype + "<")
    #if activity.atype is "action":
    if activity.atype == "action":
        print("execute name: " + activity.name)
        cont = bge.logic.getCurrentController()
        own = cont.owner

        #print("parent: " + str(own.parent))
        #print("activity: " + str(activity))
        own.playAction(activity.name, bpy.context.scene.frame_current, bpy.context.scene.frame_current + 30.0, 0, 0, 0, 0, 0.0, 0, 1.0, 2)
        #own.playAction(activity.name, 0.0, 30.0, 0, 0, 0, 0, 0.0, 0, 1.0, 2)
        bpy.context.scene.frame_current += 1
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        bpy.context.scene.update()

def update():
    """Update routine called from 'always' from Blender

    Pop the oldest activity from the queue, if existing and execute it"""
    global q

    if not q.empty():
        data = q.get()
        execute(data)
