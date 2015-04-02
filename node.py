# Copyright [2015] [Puget Sound Regional Council]

# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script manages model runs on a server by communicating with the PSRC Model Dashboard. 
# It must be running for models runs to be initiated remotely. 

# !python.exe
# ===========================
import os
import Pyro4
import time
import subprocess
import sys
import socket
import select
import threading
import shutil
import logging

logging.basicConfig(filename='node.log',level=logging.DEBUG)

class Testcase(object):
    def __init__(self):
        pass

    def runtest(self):
        for i in xrange(20):
            print "Here is some text: line " + str(i)
            with open('example_output.txt', 'w') as f:
                f.write('There is also some text in the file.')

    def runmodel(self, runid):
        ''' Start fresh model run '''
        # Create new directory 
        try:
            dirname = 'soundcast_' + str(runid)
            os.mkdir(dirname)
            os.chdir(dirname)
        except:
            return "Unable to create directory"
        
        # Clone the Soundcast repository
        repo = 'https://github.com/psrc/soundcast'
        returncode = os.system("git clone " + repo)
        if returncode == 0:
            logging.info('Cloned latest Soundcast repository')
        else:
            logging.error('Unable to clone into Soundcast repo: returncode ' + str(returncode))

        # Execute soundcast code
        os.chdir('soundcast')
        stdout_file = open('stdout.log', 'w')
        stderr_file = open('stderr.log', 'w')
        returncode = subprocess.call([sys.executable, 'run_soundcast.py'], stdout=stdout_file, stderr=stderr_file)
        stdout_file.close()
        stderr_file.close()
        if returncode == 0:
            logging.info('Completed run_soundcast.py')
        else:
            logging.error('Error running soundcast: returncode ' + str(returncode))

def main():

    print("initializing services... Server type: %s" % Pyro4.config.SERVERTYPE)

        # Start a name server and a broadcast server
    hostname = socket.gethostname()
    nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=hostname)
    assert broadcastServer is not None, "Expecting a broadcast server to be created"

    print("created nameserver, uri: %s" % nameserverUri)
    print("ns daemon location string: %s" % nameserverDaemon.locationStr)
    print("ns daemon sockets: %s" % nameserverDaemon.sockets)
    print("bc server socket: %s (fileno %d)" % (broadcastServer.sock, broadcastServer.fileno()))

    # Start a log server too

    # Create a Pyro daemon
    pyrodaemon = Pyro4.Daemon(host=hostname)
    print("daemon location string: %s" % pyrodaemon.locationStr)
    print("daemon sockets: %s" % pyrodaemon.sockets)

    # Register the server object with the daemon
    serveruri = pyrodaemon.register(Testcase())
    print("server uri: %s" % serveruri)

    # Register object with the embedded nameserver directly
    nameserverDaemon.nameserver.register(hostname, serveruri)

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
                
                # Should there just be a break here? Another branch that just starts logging model progress?
                #break
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

if __name__ == '__main__':
    main()