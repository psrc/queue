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
nodelist = ['BigBlackBox', 'PSRC3826', 'PSRC3827', 'MODELSRV2', 'MODELSRV3', 'MODELSRV4']

def check_nodes(nodelist):
    '''
    Check run state on nodes.
    0 = Available
    1 = Unavailable
    2 = Error, unable to connect
    '''

    node_dict = {}
    # Create dictionary from nodelist and check state of each node
    # Note initial state 0 assumed first, updated with check_node_state call
    for node, state in dict((node,0) for node in nodelist).iteritems():
        try:
            proxy = Pyro4.core.Proxy("PYRONAME:" + node)
            node_dict[node] = proxy.check_node_state()
        except:
            node_dict[node] = 2   # Error, unable to connect to node and/or check node state

    return node_dict

def rd_check_nodes(node_dict):
    readable_dict = {0: "Available", 1: "In Use", 2: "Connection Error"}
    result = {}
    for node, state in node_dict.iteritems():
        result[node] = readable_dict[state]

    return result

# Start model run on specified node
class StartModel:

    def __init__(self):
        pass

    def start_model(self, hostname, runid):

        # Run on any available machine from the nodelist
        for node, status in check_nodes(nodelist).iteritems():
            print node
            if status == 0:
                print "This machine is free: " + node
                print "Starting a new run here."
                proxy = Pyro4.core.Proxy("PYRONAME:" + node)
                # Run a simple test script for now
                proxy.runtest()
                break
            else:
                print node +" is unavailable, trying another node..."