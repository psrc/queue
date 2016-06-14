import Pyro4
from flask import render_template, jsonify, url_for, request
from flask_table import Table, Col, DatetimeCol
from sqlalchemy import desc
from datetime import datetime, timedelta

from plugins.pluginmount import ModelPlugin
from server import app
from server.models import RunLog


@app.route("/")
def view_index():
    if not request.args.get('sort'):
        # Default is to sort by run id, descending (most recent first)
        sort = reverse = None
        entries = RunLog.query.order_by(desc('id'))
    else:
        # Determine sort column and forward/reverse
        sort = request.args.get('sort', 'id')
        direction = request.args.get('direction', 'desc')
        reverse = (direction == 'desc')
        if direction == 'desc':
            entries = RunLog.query.order_by(desc(sort))
        else:
            entries = RunLog.query.order_by(sort)

    # Fetch most recent runs
    runtable = RunLogTable(entries, sort_by=sort, sort_reverse=reverse,
                           classes=['table','table-striped','table-hover'],
                           thead_classes=['thead-inverse'])

    # Placeholder for active nodes - client-side JS will fill this in later
    statuses = []

    return render_template('index.html',
                           user=None, runlog=runtable, nodes=statuses)


class StatusCol(Col):
    """Render a readable run status"""
    def td_format(self, content):
        if content == -1:
            # running: hourglass
            return '<span style="color:#868;"><b>&#x231b;</b></span>'
        elif content == 0:
            # success: checkmark
            return '<span style="color:#4d4;"><b>&#x2714;</b></span>'
        else:
            # failed: red flag
            return '<span style="color:#d44;">&#x1f3c1;</span>'


class RunLogTable(Table):
    """Flask Table which formats the runlog on the main page."""
    allow_sort = True

    # Columns in order of display:
    status = StatusCol('')
    id = Col('Run')
    project = Col('Project')
    series = Col('Series')
    note = Col('Notes')
    tool = Col('Model')
    # user_id = Col('User')
    start = DatetimeCol('Started')
    duration = Col('Took')

    def __init__(self, items, classes=None, thead_classes=None, sort_by=None, sort_reverse=False, no_items=None):
        super(RunLogTable, self).__init__(items, classes, thead_classes, sort_by, sort_reverse, no_items)

        # don't bother showing Model column if there is only one model plugin
        if len(ModelPlugin.get_plugins()) < 2: self.tool.show = False

    def tr_format(self, item):
        """make rows clickable"""
        url = url_for('runlog', run_id=item.id)
        return '<tr class="clickable-row" data-href="%s">{}</tr>' % url

    def sort_url(self, col_key, reverse=False):
        """create the clickable sort links in the table headers"""
        if reverse: direction = 'desc'
        else: direction = 'asc'
        return url_for('view_index', sort=col_key, direction=direction)


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


node_list = []
node_list_expires = datetime.now()  # startup time -- pre-expired!

@app.route('/nodes/')
def view_nodes():
    global node_list_expires, node_list
    if node_list_expires < datetime.now():
        with Pyro4.locateNS() as ns:
            node_list = ns.list(regex='^(?!.*NameServer).*$').keys()
            node_list.sort()
            node_list_expires = datetime.now() + timedelta(minutes=5)

    return jsonify(nodes=node_list)


@app.route('/nodes/<server_id>')
def nodestatus(server_id):
    b = node_cache.get_or_update_status(server_id)
    print str(b)
    return b #node_cache.get_or_update_status(server_id)


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


@app.route('/runlog/<int:run_id>', methods=['GET','PUT'])
def runlog(run_id=None):
    """GET: show run details.  PUT: update run exit-status"""
    log = RunLog.query.filter_by(id=run_id).first()

    if request.method == 'PUT':
        if 'status' in request.json:
            from server import db

            # update exit-status
            log.status = request.json['status']

            log.end = datetime.now()
            delta = log.end - log.start
            dur = delta.__str__()
            print dur

            # save to db
            db.session.add(log)
            db.session.commit()

            return 'OK'

    else:
        tool = ModelPlugin.get(log.tool)
        template='%s-results.html' % tool.title.lower()

        return render_template(template, log=log, tool=tool, user=None)


class NodeStatusCache(object):
    """Helper class to make node status checks take less time

    self.node ==> name: (last_checked, state, label)
    """


    def __init__(self, stale_seconds=60):
        self.lookup = {}
        self.EXPIRATION = timedelta(stale_seconds)

    def get_or_update_status(self, node):
        # Fetch if first time
        if node not in self.lookup:
            return self.update(node)

        # Fetch if stale
        last_checked, state, label = self.lookup[node]
        if datetime.now() - last_checked > self.EXPIRATION:
            return self.update(node)

        # Return cache if not stale yet
        return jsonify(node=node, state=state, label=label)

    def update(self, node):
        try:
            n = Pyro4.Proxy('PYRONAME:' + node)
            busy = n.is_busy()
            state = busy and "status-in-use" or "status-idle"
            label = busy and "IN USE" or "OK"
        except:
            # if it can't connect, big red x
            label = "ERR"
            state = "status-err"

        self.lookup[node] = (datetime.now(), state, label)
        return jsonify(node=node, state=state, label=label)

node_cache = NodeStatusCache(stale_seconds=15)
