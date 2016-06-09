import Pyro4
from flask import render_template, jsonify
from server import app
from pluginmount import ModelPlugin
from server.models import RunLog


@app.route("/")
def view_index():
    table = RunLog.query.all()

    # Placeholder for active nodes - client-side JS will fill this in later
    statuses = []

    return render_template('index.html',
                           user=None, runlog=table, nodes=statuses)


@app.route('/about/')
def view_about():
    return render_template('about.html', user=None)


@app.route('/launcher/')
def view_launcher():
    tools = ModelPlugin.get_plugins()
    return render_template('launcher.html', user=None, tools=tools)


@app.route('/login/')
def user_login(request):
    context = RequestContext(request)

    # If request is HTTP POST, try to extract user profile data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            # Is account active? It could have been disabled by the admin
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your account is disabled. Please contact an administrator.')
        else:
            # Invalid login details provided.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # Reguest is not HTTP POST, display the login form.
    else:
        return render_to_response('dashboard/login.html', {}, context)


@app.route('/logout/')
def user_logout(request):
    logout(request)

    # Return to homepage
    return HttpResponseRedirect('/')


@app.route('/monitor/')
def monitor(request):
    # Load the monitoring page
    context = RequestContext(request)

    # List of potential model server machines on local network
    nodelist = ['PSRC3827', 'MODELSRV2', 'MODELSRV3', 'MODELSRV4']

    # Show run status
    code_dict = dispatcher.check_nodes(nodelist)
    results_dict = dispatcher.rd_check_nodes(code_dict)

    return render_to_response('dashboard/monitor.html',
                              {'data': sorted(results_dict.iteritems())})


@app.route('/nodes/')
def view_nodes():
    with Pyro4.locateNS() as ns:
        nodes = ns.list(regex='^(?!.*NameServer).*$').keys()
        nodes.sort()

        return jsonify(nodes=nodes)


@app.route('/nodes/<server_id>')
def nodestatus(server_id):
    try:
        n = Pyro4.Proxy('PYRONAME:' + server_id)
        state = n.is_busy() and "status-in-use" or "status-idle"
        label = n.is_busy() and "IN USE" or "OK"
    except:
        # if it can't connect, big red x
        label = "ERR"
        state = "status-err"

    return jsonify(node=server_id, state=state, label=label)


@app.route('/register/')
def register(request):
    ''' Register new site users '''
    context = RequestContext(request)

    # Boolean to indicate if registration was successful
    registered = False

    # Only execute this view if it's posted by the user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save user's form data to the database
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Sort out the UserProfile instance. Set commit to fasle to set user attribute manually.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Save the UserProfile model instance
            profile.save()

            # Update our variable to tell the template registration was successful
            registered = True

        # Invalid form or forms?
        else:
            print user_form.errors, profile_form.errors

    # Not an HTTP POST, so render form using the ModelForm instance
    # These forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'dashboard/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


@app.route('/runlog/<int:run_id>/')
def runlog(request, run_id=None):
    '''Post: Update runlog status
    '''
    #todo This is WRONG! -- I'm using a GET instead of a POST, and I'm changing the database
    # This breaks the REST paradigm, but Django is blocking POST because of cross-site-request-forgery
    # I think.  I need to fix this, but I'm hacking it here for now because, time.

    run = RunLog.objects.get(id=int(run_id))

    # update status
    status = request.GET['status'][0]
    run.status = int(status)

    # Calculate duration
    rawtime = timezone.now() - run.start
    timedelta = datetime.timedelta(days=rawtime.days, seconds=rawtime.seconds)
    run.duration = timedelta

    # Save in Db
    run.save()

    return HttpResponseRedirect('/')
    #return render(request, 'dashboard/index.html', {'form': form})

