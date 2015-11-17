import Pyro4

from django import forms
from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from dashboard.forms import is_valid_file, is_node_free
from dashboard.plugin import Plugin
from dashboard.tool import Tool


def view_soundcast(cls, request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SoundcastRunsForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data

            # Fetch host, so we can build an update URL on the other side
            host = request.get_host()

            tool = Plugin(request, form.cleaned_data)
            tool.set_plugin(name='SoundCast',
                            script ='dashboard/plugins/soundcast.script',
                            freezer='dashboard/plugins/soundcast-freezer.bat',
                            host=host)
            tool.run_model()

            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            print "invalid form is invalid."

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SoundcastRunsForm()

    return render(request, 'dashboard/soundcast.html', {'form': form})

class SoundcastRuns(models.Model):
    runid = models.CharField(max_length=240, db_index=True)


class SoundcastRunsForm(forms.Form):
    project = forms.CharField(max_length=100)
    notes = forms.CharField(label='Run notes', max_length=512, required=False)
    tag = forms.CharField(label='Git tag', max_length=64)
    configuration = forms.FileField(label='Input configuration',
            validators=[is_valid_file], required=False)

    # get list of nodes from nameserver, but don't list nameserver itself
    node = forms.ChoiceField(label='Run on',
            choices=[(x, x) for x in Pyro4.locateNS().list().keys() if 'NameServer' not in x],
            validators=[is_node_free], required=True)

class SoundCast(Tool):
    """ PSRC SoundCast activity-based model plugin """
    title = 'SoundCast'
    form = SoundcastRunsForm
    dbtable = SoundcastRuns
    view = view_soundcast
