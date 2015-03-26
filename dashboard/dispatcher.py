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

# List of potential model server machines on local network
serverlist =  ['MODELSRV' + str(i) for i in xrange(1,5)]

# Placeholder for Run ID
runid = np.random.randint(1, 10000)

# Start the model run on the modelserver
class StartModel():
    def start_model(self, hostname):
        try:
            proxy = Pyro4.core.Proxy("PYRONAME:" + hostname)
            proxy.runmodel(runid)
            print "Started model run on: " + hostname

            return runid

        except:
            print sys.exc_info()
            #traceback.print_exc()
            print "Couldn't connect to: " + hostname


# Try connecting to a server
for host in serverlist:
    print 'trying to run on ' + host
    try: 
        start_model(host)
    except:
        "Not connected to: " + host