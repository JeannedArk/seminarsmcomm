import bge
import time
import socket
import asyncio

# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 23000
# Die Konstante AF_INET steht für Adressfamilie Internet.
# Die Konstante SOCK_DGRAM steht für das UDP-Protokoll.
# Dies sind optionale Eingaben für eine Socket-Instanz.
# Voreingestellt ist AF_INET und als Protokoll SockStream, dies steht für
# ein TPC-socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#loop = asyncio.get_event_loop()

finished = False


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
    if not finished:
        try:
            #while 1:    # Endlosschleife
            # buffer size must be a power of 2
            data, addr = sock.recvfrom(1024)
            print("Received msg:", data)
            print("Clientadresse:", addr)         # Adresse besteht aus IP und Port
        except socket.error:
            print("socket timeout " + sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info()[0])

def send(msg):
    print("Message:", msg)
    sock.sendto(msg, (UDP_IP, UDP_PORT))
