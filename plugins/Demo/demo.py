from pluginmount import ModelPlugin

name = 'Demo'
script = 'dashboard/plugins/Demo/demo.script'
freezer = 'dashboard/plugins/Demo/demo-freezer.bat'
template = 'dashboard/demo.html'


def view_demo(cls): #, request):
    return "hiii"

def cheem(cls, request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = None #DemoForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data

            # Fetch host, so we can build an update URL on the other side
            host = request.get_host()

            tool = None #Plugin(request, form.cleaned_data)
            tool.set_plugin(name=name,
                            script =script,
                            freezer=freezer,
                            host=host)
            tool.run_model()

            # redirect to a new URL:
            return None #HttpResponseRedirect('/')
        else:
            print "invalid form is invalid."

    # if a GET (or any other method) we'll create a blank form
    else:
        pass # form = DemoForm()

    return "hiii" # None #render(request, template, {'form': form})



class Demo(ModelPlugin):
    """ PSRC SoundCast activity-based model plugin """
    title = 'Demo'
    form = None # DemoForm
    dbtable = None
    view = view_demo
