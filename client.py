# This should be running on all model servers

import Pyro4
import time
import subprocess
import sys
import socket
import select

hostname = socket.gethostname()

class Testcase(object):
    def __init__(self):
        self.value = 1

    def runmodel(self):
        print ("Running some test code. You should see the text file 'itworked.txt now")
        subprocess.call([sys.executable, 'test.py'])

print("initializing services... Server type: %s" % Pyro4.config.SERVERTYPE)

# Start a name server and a broadcast server
nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=hostname)
assert broadcastServer is not None, "Expecting a broadcast server to be created"

print("got a Nameserver, uri: %s" % nameserverUri)
print("ns daemon location string: %s" % nameserverDaemon.locationStr)
print("ns daemon sockets: %s" % nameserverDaemon.sockets)
print("bc server socket: %s (fileno %d)" % (broadcastServer.sock, broadcastServer.fileno()))

# Create a Pyro daemon
pyrodaemon = Pyro4.Daemon(host=hostname)
print("daemon location string: %s" % pyrodaemon.locationStr)
print("daemon sockets: %s" % pyrodaemon.sockets)

# Register the server object with the daemon
serveruri = pyrodaemon.register(Testcase())
print("server uri: %s" % serveruri)

# Register object with the embedded nameserver directly
nameserverDaemon.nameserver.register("test", serveruri)

print("")

# Wait to be called by dispatcher
while True:
    print("Waiting for events...")
    # Create sets of the expected socket objects
    nameserverSockets = set(nameserverDaemon.sockets)
    pyroSockets = set(pyrodaemon.sockets)
    rs = [broadcastServer]  # only the broadcast server is directly usable as a select() object
    rs.extend(nameserverSockets)
    rs.extend(pyroSockets)
    rs,_,_ = select.select(rs,[],[],3)
    eventsForNameserver = []
    eventsForDaemon = []
    for s in rs:
        if s is broadcastServer:
            print("Broadcast server received a request")
            broadcastServer.processRequest()
        elif s in nameserverSockets:
            eventsForNameserver.append(s)
        elif s in pyroSockets:
            eventsForDaemon.append(s)
    if eventsForNameserver:
        print("Nameserver received a request")
        nameserverDaemon.events(eventsForNameserver)
    if eventsForDaemon:
        print("Daemon received a request")
        pyrodaemon.events(eventsForDaemon)

nameserverDaemon.close()
broadcastServer.close()
pyrodaemon.close()
print("done")