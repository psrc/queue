# Copyright (c) 2015 Puget Sound Regional Council, Seattle WA USA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This script manages model runs on a server by communicating with the PSRC Model Dashboard.
# It must be running for models runs to be initiated remotely.
#
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

logging.basicConfig(filename='node.log', level=logging.DEBUG)

class Node(object):
    busy = False
    command = None
    p = None
    cwd = None
    returncode = -1

    def __init__(self):
        self.name = socket.gethostname()
        logging.info('##############################################')
        logging.info('i am: '+self.name)


    def is_busy(self):
        return self.busy

    def is_available(self):
        return not self.busy

    def kill(self):
        '''
        Kill a running command, if there is one
        '''
        if self.p:
            logging.info('terminating: '+str(self.command))
            self.p.terminate()
        else:
            logging.info('nothing to terminate.')


    def status(self):
        '''
        Get node status
        Returns tuple: (returncode, busy, command, working_dir)
        returncode=-1 if process has not returned yet
        '''
        return (self.returncode, self.busy, self.command, self.cwd)


    def runandwait(self, command, cwd=None):
        '''
        Spawn a subprocess. Wait for task to finish, and return the process returncode.
        '''
        self.start(command, cwd, wait=True)


    def start(self, command, cwd=None, wait=False):
        '''
        Spawn a subprocess. Return immediately.
        '''
        if self.busy:
            logging.error('# Already busy, running: '+str(command))
            raise RuntimeError("Already busy")
            return

        logging.info('----------------------------------------------')
        logging.info('received command: '+str(command))

        self.busy = True
        self.command = command
        self.cwd = cwd
        self.returncode = -1

        # Launch the process, and save a handle to it in self.p
        self.popenAndCall(self.onExit, command, cwd, wait)


    def onExit(self, returncode):
        """
        Callback function which is run when a subprocess is completed.
        Resets busy flag and gets node ready for the next run.
        """
        logging.info("ON-EXIT: return code "+ str(returncode) + " : " + str(self.command))

        self.returncode = returncode
        self.busy = False
        self.p = None
        self.command = None
        self.cwd = None

        if (returncode>0):
            raise RuntimeError('Failed: return code '+str(returncode))


    def popenAndCall(self, onExit, command, cwd, wait):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes.
        onExit is a callable object, and popenArgs is a list/tuple of args that
        would give to subprocess.Popen.
        """
        def runIt(onExit, command):
            rtncode = -1

            # Put log files in cwd folder
            pout = 'stdout.log'
            if cwd:
                pout = os.path.join(cwd, pout)

            try:
                with open(pout, 'a') as file_out:
                    self.p = subprocess.Popen(command, cwd=cwd, stdout=file_out, stderr=subprocess.STDOUT)
                    self.p.wait()
                    rtncode = self.p.returncode
            except:
                rtncode = 8
            finally:
                onExit(rtncode)

        if wait:
            runIt(onExit, command)
        else:
            thread = threading.Thread(target=runIt, args=(onExit, command))
            thread.start()


def runtests():
    n = Node()

    cmd = ["ipconfig.exe"]
    n.start(cmd, r"c:\users\zbilly")
    time.sleep(1)
    print n.status()
    n.start(cmd)
    time.sleep(1)
    n.kill()


def main():
    n = Node()

    # Start Pyro -- requires one Pyro Name server on network somewhere
    # To start a Pyro Name Server, do "pyro4-ns.exe -n [hostname]"

    Pyro4.Daemon.serveSimple({ n : n.name } , host=n.name, ns=True)


if __name__ == '__main__':
    #runtests()
    main()
