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
SceneMakerCommunication retreives all data sent from the current running
Visual SceneMaker instance (http://scenemaker.dfki.de/getstarted.html).
The data is sent in JSON with ActionActivity and SpeechActivity objects.

Therefore it creates a socket with the defined configuration. The retreived
activities will be further propagated to Blender.

Note: Executing the SpeechActivity is not yet implemented, but should be
relatively easy if the connection with MaryTTS works.



playAction documentation:
https://docs.blender.org/api/blender_python_api_2_60_1/bge.types.html

playAction(name, start_frame, end_frame, layer=0, priority=0, blendin=0, play_mode=ACT_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1.0)

- layer (integer) – the layer the action will play in (actions in different layers are added/blended together)
- priority (integer) – only play this action if there isn’t an action currently playing in this layer with a higher (lower number) priority
- blendin (float) – the amount of blending between this animation and the previous one on this layer
- play_mode (KX_ACTION_MODE_PLAY, KX_ACTION_MODE_LOOP, or KX_ACTION_MODE_PING_PONG) – the play mode



Some helpful debugging parameters:
bge.logic.getCurrentController().owner.getActionFrame()
bge.logic.getCurrentController().owner.isPlayingAction()
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


def execute(activity):
    """Execute the passed activity. It is either a SpeechActivity or ActionActivity

    Note: Executing the SpeechActivity is not yet implemented, but should be relatively easy
    if the connection with MaryTTS works.
    """

    print("execute: " + str(activity))
    if activity.atype == "action":
        print("execute name: " + activity.name)
        cont = bge.logic.getCurrentController()
        own = cont.owner

        # TODO get from activity?
        start_frame = 0
        end_frame = 30
        own.playAction(activity.name, start_frame, end_frame, play_mode=bge.logic.KX_ACTION_MODE_PLAY, speed=0.5)


def update():
    """Update routine called from 'always' from Blender

    Pop the oldest activity from the queue, if existing and execute it"""
    global q

    # TODO test with several animations
    # it will be probably not playing overlapping animations
    # then check if one animation is still playing, then
    # pop the activity from the queue

    if not q.empty():
        data = q.get()
        execute(data)