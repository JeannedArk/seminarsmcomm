import asyncio
import socket


#Example taken from
#https://docs.python.org/3/library/asyncio-eventloop.html



# UDP setup
UDP_IP = "127.0.0.1"
UDP_PORT = 23000

# Create a pair of connected file descriptors
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())
    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)
    # Stop the event loop
    loop.stop()

# Register the file descriptor for read event
loop.add_reader(rsock, reader)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

# Run the event loop
loop.run_forever()

# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()
