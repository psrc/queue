# Copyright [2014] [Puget Sound Regional Council]

# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !python.exe
# PSRC Model Run Dispatcher
# ===========================
import os
import sys
import Pyro4
import numpy as np
import pickle
import logging, logging.handlers
import SocketServer
import struct
import subprocess

# List of potential model server machines on local network
#serverlist =  ['MODELSRV' + str(i) for i in xrange(1,5)]
serverlist = ['PSRC3827']

# Placeholder for Run ID
# Want the user to be able to define this ID, or use a datetime stamp
runid = np.random.randint(1, 10000)

# Start the model run on the modelserver
class StartModel():
    def start_model(self, hostname, runid):
        
        # Start a logging mini-server
        subprocess.Popen([sys.executable, 'log_server.py'], stdin=None, stdout=None, stderr=None)


        ###########
        rootLogger = logging.getLogger('')
        socketHandler = logging.handlers.SocketHandler('localhost',
                            logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        # don't bother with a formatter, since a socket handler sends the event as
        # an unformatted pickle
        rootLogger.addHandler(socketHandler)

        # Now, we can log to the root logger, or any other logger. First the root...
        logging.info('Jackdaws love my big sphinx of quartz.')

        # Now, define a couple of other loggers which might represent areas in your
        # application:

        logger1 = logging.getLogger('myapp.area1')
        logger2 = logging.getLogger('myapp.area2')

        logger1.debug('Quick zephyrs blow, vexing daft Jim.')
        logger1.info('How quickly daft jumping zebras vex.')
        logger2.warning('Jail zesty vixen who grabbed pay from quack.')
        logger2.error('The five boxing wizards jump quickly.')

        print('Connecting to node...')
        try:
            #sys.stdout = open('file', 'w')
            proxy = Pyro4.core.Proxy("PYRONAME:" + hostname)
            
            SocketServer.StreamRequestHandler
            
            proxy.runmodel(runid)
            print "Started model run on: " + hostname

            return runid

        except:
            print sys.exc_info()
            #traceback.print_exc()
            print "Couldn't connect to: " + hostname