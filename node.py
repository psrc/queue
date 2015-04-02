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
        self.node_state = 0

    def check_node_state(self):
        ''' Pyro won't expose private methods, so we need a public method to check node state '''
        return self.node_state

    @Pyro4.oneway   # decorator implies we don't wait for return before executing next code lines
    def runtest(self):
        ''' Example test function that write text to file, runs for several minutes '''
        self.node_state = 1         # Node is busy
        for i in xrange(20):
            print "Here is some text: line " + str(i)
            time.sleep(30)          # Stretch this out so we can test a continual process
            with open('example_output.txt', 'w') as f:
                f.write('There is also some text in the file.')
        self.node_state = 0         # Node is free for now



    @Pyro4.oneway
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

    logging.info('Started node on %s' %  socket.gethostname())
    logging.info("initializing services... Server type: %s" % Pyro4.config.SERVERTYPE)

        # Start a name server and a broadcast server
    nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=socket.gethostname())
    assert broadcastServer is not None, "Expecting a broadcast server to be created"

    logging.info("created nameserver, uri: %s" % nameserverUri)
    logging.info("ns daemon location string: %s" % nameserverDaemon.locationStr)
    logging.info("ns daemon sockets: %s" % nameserverDaemon.sockets)
    logging.info("bc server socket: %s (fileno %d)" % (broadcastServer.sock, broadcastServer.fileno()))

    # Create a Pyro daemon
    pyrodaemon = Pyro4.Daemon(host=socket.gethostname())
    logging.info("daemon location string: %s" % pyrodaemon.locationStr)
    logging.info("daemon sockets: %s" % pyrodaemon.sockets)

    # Register the server object with the daemon
    serveruri = pyrodaemon.register(Testcase())
    logging.info("server uri: %s" % serveruri)

    # Register object with the embedded nameserver directly
    nameserverDaemon.nameserver.register(socket.gethostname(), serveruri)

    logging.info("")

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