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
import logcontroller

# Save standard output to a text file
sys.stdout = open('file', 'w')

class Testcase(object):
    def __init__(self):
        pass

    def runmodel(self, runid):
        ''' Start fresh model run '''
        # Create new directory 
        try:
            dirname = 'soundcast_' + str(runid)
            os.mkdir(dirname)
            os.chdir(dirname)
        except:
            return "Unable to create directory"

        # Create a new log file
        logger = logcontroller.setup_custom_logger(str(runid))
        logger.info('Run ID: ' + str(runid))
        
        # Clone the Soundcast repository
        repo = 'https://github.com/psrc/soundcast'
        returncode = os.system("git clone " + repo)
        if returncode == 0:
            logger.info('Cloned latest Soundcast repository')
        else:
            logger.error('Unable to clone into Soundcast repo: returncode ' + str(returncode))

        # Execute soundcast code
        os.chdir('soundcast')
        returncode = subprocess.call([sys.executable, 'run_soundcast.py'])
        if returncode == 0:
            logger.info('Started run_soundcast.py')
        else:
            logger.error('Error starting run_soundcast: returncode ' + str(returncode))

        return logger

# Find space to run the model
#NUMCPU = int(os.getenv("NUMBER_OF_PROCESSORS"))
#CPURunner = threading.Semaphore(NUMCPU)
#runner = CPURunner.acquire()  # block, until a CPU is free

## All done with this jobqueue, let's give the CPU back and exit.
#CPURunner.release()

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