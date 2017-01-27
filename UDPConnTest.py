import asyncio
import socket


#Example taken from
#https://docs.python.org/3/library/asyncio-eventloop.html
#https://wiki.python.org/moin/UdpCommunication


# UDP setup
#UDP_IP = "127.0.0.1"
UDP_IP = "192.168.0.255"
UDP_PORT = 23000

# not SOCK_STREAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(64) # buffer size is 1024 bytes
    print("received message:", data)
