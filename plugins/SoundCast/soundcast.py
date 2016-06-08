import Pyro4, urlparse
from flask import request, render_template, redirect
from flask_wtf import Form
from wtforms import validators, StringField, FileField, SelectField, SubmitField
import forms

from pluginmount import ModelPlugin
from plugin import Plugin


def view_soundcast(cls):
    print "HIYEEE"

    form = SoundcastRunsForm()
    if request.method == 'POST':
        print 'POST!!!'
        if form.validate():
            print form.data

            # Parse host, so we can build an update URL on the other side
            host_url = urlparse.urlparse(request.url)
            host = "%s:%d" % (host_url.hostname, host_url.port)
            print host

            tool = Plugin(form.data)
            tool.set_plugin(name='SoundCast',
                            script ='/plugins/soundcast.script',
                            freezer='/plugins/soundcast-freezer.bat',
                            host=host)

            # spawn model and redirect to the main index
            tool.run_model()
            return redirect('/')

        else:
            print "invalid form is invalid."

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SoundcastRunsForm()

    return render_template('soundcast.html', user=None, form=form)


class SoundcastRunsForm(Form):
    project = StringField('Project', [validators.InputRequired(),
                                      validators.Length(max=50)])

    notes = StringField('Run notes', [validators.Length(max=512)])

    tag = StringField('Git tag', [validators.Length(max=512)])

    configuration = FileField('Input configuration', [validators.InputRequired()])

    node = SelectField(label='Run on', validators=[forms.verify_node_is_free])

    submit = SubmitField('Start Run')

    # add node dropdown
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        # get list of nodes from nameserver, but don't list nameserver itself
        try:
            all_nodes = Pyro4.locateNS().list().keys()
        except:
            all_nodes = ['Nameserver not found']

        self.node.choices = [(x, x) for x in all_nodes if 'NameServer' not in x]


class SoundCast(ModelPlugin):
    """ PSRC SoundCast activity-based model plugin """
    view = view_soundcast
    title = 'SoundCast'
    form = SoundcastRunsForm
    dbtable = None # todo SoundcastRuns
