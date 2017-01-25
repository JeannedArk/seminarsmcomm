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
    print("UDPSceneMakerCommunication init")
    bge.render.showMouse(True)

def keypressed():
    print("key pressed")

def update():
