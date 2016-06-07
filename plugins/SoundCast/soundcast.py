import Pyro4

from flask import request, render_template

from flask_wtf import Form
from wtforms import validators, StringField, FileField, SelectField

from pluginmount import ModelPlugin
import forms

def view_soundcast(cls):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SoundcastRunsForm()
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data

            # Fetch host, so we can build an update URL on the other side
            host = request.get_host()

            tool = None #Plugin(request, form.cleaned_data)
            tool.set_plugin(name='SoundCast',
                            script ='dashboard/plugins/soundcast.script',
                            freezer='dashboard/plugins/soundcast-freezer.bat',
                            host=host)
            tool.run_model()

            # redirect to a new URL:
            return None #HttpResponseRedirect('/')
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

    # get list of nodes from nameserver, but don't list nameserver itself
    try:
        node = SelectField(label='Run on',
                           choices=[(x, x) for x in Pyro4.locateNS().list().keys() if 'NameServer' not in x],
                           validators=[forms.verify_node_is_free], required=True)
    except:
        pass  # nameserver might not be up yet


class SoundCast(ModelPlugin):
    """ PSRC SoundCast activity-based model plugin """
    view = view_soundcast
    title = 'SoundCast'
    form = SoundcastRunsForm
    dbtable = None # todo SoundcastRuns
