# mymodeltool.py -- contains everything to run a particular model or tool.
# copy to yourname.py and edit as needed.

import Pyro4
import logging, socket

from dashboard.models import RunLog, Tool

logger = logging.getLogger(socket.gethostname())

# SOUNDCAST tool
class Plugin(object):

    def __init__(self, request, data):
        self.request = request
        self.project = data['project']
        self.tag = data['tag']

    def run_model(self):
        '''
        Clone soundcast into the working folder, then run the model commands in that folder.
        '''

        series = self.get_next_series(self.project)
        tool = Tool.objects.get(name='SoundCast')

        self.addLogEntry(self.project, series, tool, self.tag)

        n = Pyro4.Proxy('PYRONAME:PSRC3826')

        logger.info('spawning')
        n.runandwait('git clone git@github.com:psrc/model-dashboard.git \"{}/{}\"'.format(self.project, series))
        #n.start('python.exe run_soundcast.py', self.project)
        print 'done'

    def addLogEntry(self, project, series, tool, tag):
        logger.info('adding log entry: ' + self.project + '/' + series)

        run = RunLog(user=self.request.user,
            project=project, series=series, tool=tool, tool_tag=tag)
        run.save()


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

        print "series:", series

        return series
