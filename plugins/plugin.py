from datetime import datetime
import Pyro4

from server.models import RunLog, User
from server import db


class Plugin(object):
    def __init__(self, data):
        self.project = data['project']
        self.notes = data['notes']
        self.tag = data['tag']
        self.node = data['node']

        # Plugin instance must populate these
        self.name = None
        self.script = None
        self.snapshot = None
        self.host = None
        

    def set_plugin(self, name=None, script=None, snapshot=None, host=None, plugin_inputs=None):
        self.name = name
        self.script = script
        self.snapshot = snapshot
        self.host = host
        self.plugin_inputs = plugin_inputs    # key-value pairs for unique plugin form fields

    def run_model(self, form):
        """
        yeah run that model!
        """

        # plugin_inputs = self.plugin_inputs
        tool = self.name
        series = self.get_next_series(self.project)

        # create the log entry
        run = self.add_log_entry(tool, series)

        # fetch script lines
        with open(self.script) as f:
            lines = f.readlines()

        # fetch freezer lines
        with open(self.snapshot) as f:
            freezer_lines = f.readlines()

        # todo - attempt to dial a node
        n = Pyro4.Proxy('PYRONAME:' + str(self.node))

        # Expected environment variables
        replacements = {}
        replacements['TAG'] = self.tag
        replacements['QUEUE_RUN_ID'] = run
        for field_name, field_value in self.plugin_inputs.iteritems():
            replacements[field_name] = field_value

        # and run the fluffy
        n.runscript(lines, freezer_lines, self.project, series,
                    run_id=run, replacements=replacements, host=self.host)

    def add_log_entry(self, tool, series):
        """
        Add an entry to the run log for this project
        Returns the id of the entry
        """
        run = RunLog(user=None, project=self.project, series=series,
                     note=self.notes, tool=tool, tool_tag=self.tag,
                     status=-1, start=datetime.now(), node=self.node)

        db.session.add(run)
        db.session.commit()

        return run.id

    @staticmethod
    def get_next_series(project):
        """
        Determine the next AA-style series for a project
        """
        num_projects = RunLog.query.filter_by(project=project).count()
        series = Plugin.get_series_from_count(num_projects)
        return series

    @staticmethod
    def get_series_from_count(count):
        """
        Convert an integer to an AA-style series (AA,  AB, AC, etc)
        """
        capital_a = ord('A')

        a = count / 676
        b = (count - a * 676) / 26
        c = count % 26

        series = ''
        if a: series += chr(a + capital_a - 1)
        series += chr(b + capital_a)
        series += chr(c + capital_a)

        return series
