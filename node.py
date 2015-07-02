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
import requests

logger = logging.getLogger(socket.gethostname())

class Node(object):
    busy = False
    command = None
    p = None
    cwd = None
    returncode = -1
    run_id = None
    host = None

    def __init__(self):
        self.name = socket.gethostname()
        logger.info('##############################################')
        logger.info('i am: '+self.name)
        logger.info('working dir: '+os.getcwd())


    def is_busy(self):
        return self.busy


    def is_available(self):
        return not self.busy


    def create_dir(self, path, subdir=None):
        '''
        Create a directory, with optional subdirectory
        '''
        fullpath = path
        if subdir:
            fullpath = os.path.join(path, subdir)

        try:
            os.makedirs(fullpath)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(fullpath):
                pass
            else: raise


    def kill(self):
        '''
        Kill a running command, if there is one
        '''
        if self.p:
            logger.info('terminating: '+str(self.command))
            self.p.terminate()
        else:
            logger.info('nothing to terminate.')


    def status(self):
        '''
        Get node status
        Returns tuple: (returncode, busy, command, working_dir)
        returncode=-1 if process has not returned yet
        '''
        return (self.returncode, self.busy, self.command, self.cwd)


    def runscript(self, lines, freezer, project, series, run_id=None, replacements={}, host=None):
        '''
        Take a list of script lines, and run them in a unique folder.
        Folder name formed from project & series.
        '''
        logger.info('----------------------------------------------')
        logger.info('Runscript called!')

        self.create_dir(project, series)

        if host: self.host = host

        # Write script file
        filepath = os.path.join(project, series, 'run.bat')
        with open(filepath, 'w') as script:
            script.writelines(lines)

        # Write freezer file
        filepath = os.path.join(project, series, 'freezer.bat')
        with open(filepath, 'w') as frz:
            frz.writelines(freezer)


        cmd = 'run.bat'
        self.start(cmd, project, series, run_id, replacements=replacements)


    def runandwait(self, command, project, series, run_id=None, replacements={}):
        '''
        Spawn a subprocess. Wait for task to finish, and return the process returncode.
        '''
        self.start(command, project, series, run_id=run_id, wait=True, replacements=replacements)


    def start(self, command, project, series, run_id=None, replacements={}, wait=False):
        '''
        Spawn a subprocess. Return immediately.
        '''
        if self.busy:
            logger.error('# Already busy, running: '+str(command))
            raise RuntimeError("Already busy")
            return

        logger.info('received command: '+str(command))
        logger.info("start: run_id is " + str(run_id))

        cwd = os.path.join(project, series)

        self.busy = True
        self.command = command
        self.cwd = cwd
        self.returncode = -1
        self.run_id=run_id

        # Launch the process, and save a handle to it in self.p
        self.popenAndCall(self.onExit, command, project, series, wait, replacements)


    def onExit(self, returncode):
        """
        Callback function which is run when a subprocess is completed.
        Resets busy flag and gets node ready for the next run.
        """
        logger.info("ON-EXIT: return code "+ str(returncode) + " : " + str(self.command))

        self.returncode = returncode
        self.busy = False
        self.p = None
        self.command = None
        self.cwd = None

        # Update run log with status
        if self.run_id:
            data = {'status': returncode}

            # Build URL from host and run_id
            url = 'http://' + self.host + '/runlog/' + str(self.run_id)
            print 'Updating via ', url
            response = requests.get(url, params=data)

            logger.info('updated status for run ' + str(self.run_id) + ': response ' + str(response))

        if (returncode>0):
            pass #raise RuntimeError('Failed: return code '+str(returncode))


    def popenAndCall(self, onExit, command, project, series, wait, replacements):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes. onExit is a callable object.
        """
        # Populate any needed environment variables that were passed in
        # all hail unicode! thanks python 2.
        env = os.environ.copy()
        for k,v in replacements.iteritems():
            env[str(k)] = str(v)

        def runIt(onExit, command):
            rtncode = -1

            # Working directory is project/series
            cwd = os.path.join(project, series)
            # Log file
            plogfile = os.path.join(project, series, 'stdout.log')

#            try:
            with open(plogfile, 'a') as file_out:
                    self.p = subprocess.Popen('cmd /c run.bat', cwd=cwd, env=env, stdout=file_out, stderr=subprocess.STDOUT)
                    self.p.wait()
                    rtncode = self.p.returncode
#            except:
#                rtncode = 8
#            finally:
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

def set_high_priority():
    '''
    Run node code at extra-high priority, so it stays responsive even
    while models are running.
    '''
    import platform
    if platform.system()=='Windows':
        print 'Setting Windows process priority'
        import win32api, win32process, win32con
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)


def setup_logger():
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('node.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s/%(name)s %(levelname)s %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def main():
    set_high_priority()
    setup_logger()

    # Start Pyro -- requires one Pyro Name server on network somewhere
    n = Node()

    try:
        Pyro4.Daemon.serveSimple({ n : n.name } , host=n.name, ns=True)
    except:
        print('\n###\nNo Pyro name server found on local network.')
        print("To start a Pyro Name Server, do 'pyro4-ns.exe -n [hostname]'")


if __name__ == '__main__':
    #runtests()
    main()
