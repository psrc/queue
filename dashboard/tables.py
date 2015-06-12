import django_tables2 as tables
from .models import RunLog

class RunLogTable(tables.Table):
    class Meta:
        model = RunLog
        exclude = ['group', 'inputs']
        attrs = {"class": "paleblue"}
