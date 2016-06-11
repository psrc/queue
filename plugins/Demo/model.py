import urlparse

import Pyro4
from flask import request, render_template, redirect
from flask_wtf import Form
from wtforms import validators, StringField, FileField, SelectField, SubmitField

from server import forms
from server.plugin import Plugin
from server.pluginmount import ModelPlugin

name =     'Demo'
script   = 'plugins/Demo/demo.script'
snapshot = 'plugins/Demo/demo-snapshot.bat'


def view_demo_launcher(cls):
    form = DemoLauncherForm()
    if request.method == 'POST':
        if form.validate():
            # Parse host, so we can build an update URL on the other side
            host_url = urlparse.urlparse(request.url)
            host = host_url.hostname
            if host_url.port: host += ":"+str(host_url.port)

            tool = Plugin(form.data)
            tool.set_plugin(name=name,
                            script=script,
                            snapshot=snapshot,
                            host=host)

            # spawn model and redirect to the main index
            tool.run_model()
            return redirect('/')

        else:
            print "invalid form is invalid."

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DemoLauncherForm()

    return render_template('demo.html', user=None, form=form)


class DemoLauncherForm(Form):
    project       = StringField('Project', [validators.InputRequired(), validators.Length(max=50)])

    notes         = StringField('Run notes', [validators.Length(max=512)])

    tag           = StringField('Git tag', [validators.Length(max=512)])

    node          = SelectField(label='Run on', validators=[forms.verify_node_is_free])

    submit        = SubmitField('Start Run')

    # add node dropdown items
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        # get list of nodes from nameserver, but don't list nameserver itself
        try:
            all_nodes = Pyro4.locateNS().list().keys()
        except:
            all_nodes = ['Nameserver not found']

        self.node.choices = [(x, x) for x in all_nodes if 'NameServer' not in x]


class Demo(ModelPlugin):
    """ PSRC SoundCast activity-based model plugin """
    title = 'Demo'
    description = "Sample plugin"
    image = 'img/4k.png'
    url = 'http://www.queue-project.org'
    form = DemoLauncherForm
    dbtable = None
    launcher = view_demo_launcher
