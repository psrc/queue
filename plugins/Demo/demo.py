import Pyro4
from django import forms
from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from dashboard.forms import is_valid_file, is_node_free
from dashboard.plugin import Plugin
from dashboard.plugins.SoundCast.soundcast import SoundcastRuns
from dashboard.tool import Tool

name = 'Demo'
script = 'dashboard/plugins/Demo/demo.script'
freezer = 'dashboard/plugins/Demo/demo-freezer.bat'
template = 'dashboard/demo.html'


def view_demo(cls, request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DemoForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data

            # Fetch host, so we can build an update URL on the other side
            host = request.get_host()

            tool = Plugin(request, form.cleaned_data)
            tool.set_plugin(name=name,
                            script =script,
                            freezer=freezer,
                            host=host)
            tool.run_model()

            # redirect to a new URL:
            return HttpResponseRedirect('/')
        else:
            print "invalid form is invalid."

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DemoForm()

    return render(request, template, {'form': form})


class DemoRuns(models.Model):
    runid = models.CharField(max_length=240, db_index=True)


class DemoForm(forms.Form):
    project = forms.CharField(max_length=100)
    notes = forms.CharField(label='Run notes', max_length=512, required=False)
    tag = forms.CharField(label='Git tag', max_length=64, required=False)
    configuration = forms.FileField(label='Input configuration',
            validators=[is_valid_file], required=False)

    # get list of nodes from nameserver, but don't list nameserver itself
    try:
        node = forms.ChoiceField(label='Run on',
            choices=[(x, x) for x in Pyro4.locateNS().list().keys() if 'NameServer' not in x],
            validators=[is_node_free], required=True)
    except:
        pass  # nameserver might not be up yet



class Demo(Tool):
    """ PSRC SoundCast activity-based model plugin """
    title = 'Demo'
    form = DemoForm
    dbtable = SoundcastRuns
    view = view_demo
