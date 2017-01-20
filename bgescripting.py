import bge
import time
import socket
import asyncio

# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 23000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
https://docs.python.org/3/library/asyncio-eventloop.html
https://docs.python.org/2/howto/sockets.html
"""

def init():
    global last_time
    print("Hello")
    bge.render.showMouse(True)

    last_time = time.time()

def keypressed():
    global myx
    #global scene
    print("key pressed")

    myx += 0.1
    print(str(myx))

    co = bge.logic.getCurrentController()
    obj = co.owner
    obj.localPosition.x += 0.05

    scene = obj.scene
    cube = scene.objects["Cube"]
    cube.localPosition.z += 0.2

def update():
    global last_time
    now = time.time()

    dt = now - last_time
    print("dt="+str(dt))

    last_time = now
