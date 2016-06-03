from pluginmount import ModelPlugin

def view_soundcast(cls):
    return 'SOUNDCAST!!!'

def junk(cls, request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = None #SoundcastRunsForm(request.POST, request.FILES)
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
        pass #form = SoundcastRunsForm()

    return None #render(request, 'dashboard/soundcast.html', {'form': form})


class SoundCast(ModelPlugin):
    """ PSRC SoundCast activity-based model plugin """
    title = 'SoundCast'
    form = None #SoundcastRunsForm
    dbtable = None #SoundcastRuns
    view = view_soundcast
