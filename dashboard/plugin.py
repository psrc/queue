import Pyro4
import logging, socket
from datetime import datetime

from dashboard.models import RunLog, Tool

class Plugin(object):

    def __init__(self, request, data):
        self.request = request
        self.project = data['project']
        self.tag = data['tag']
        self.node = data['node']

        # Plugin instance must populate these
        self.name = None
        self.script = None


    def set_plugin(self, name=None, script=None):
        self.name = name
        self.script = script


    def run_model(self):
        '''
        yeah run that model!
        '''
        tool = Tool.objects.get(name=self.name)
        series = self.get_next_series(self.project)

        # fetch script lines
        with open(self.script) as f:
            lines = f.readlines()

        #todo - attempt to dial a node
        n = Pyro4.Proxy('PYRONAME:' + str(self.node))

        # create the log entry
        run = self.addLogEntry(self.project, series, tool, self.tag)

        # Expected environment variables
        replacements = {}
        replacements['TAG'] = self.tag

        # and run the fluffy
        n.runscript(lines, self.project, series, run_id=run, replacements=replacements)


    def addLogEntry(self, project, series, tool, tag):
        '''
        Add an entry to the run log for this project
        Returns the id of the entry
        '''
        run = RunLog(user=self.request.user, project=project,
            series=series, tool=tool, tool_tag=tag, start=datetime.now())
        run.save()

        return run.id


    def get_next_series(self, project):
        '''
        Determine the next AA-style series for a project
        '''
        num_projects = RunLog.objects.filter(project=project).count()
        series = self.get_series_from_count(num_projects)
        return series


    def get_series_from_count(self, count):
        '''
        Convert an integer to an AA-style series (AA,  AB, AC, etc)
        '''
        capital_a = ord('A')

        a = count / 676
        b = (count - a * 676) / 26
        c = count % 26

        series = ''
        if (a): series += chr(a+capital_a - 1)
        series += chr(b+capital_a)
        series += chr(c+capital_a)

        return series
