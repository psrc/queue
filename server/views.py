from flask import render_template

from server import app, plugins


@app.route("/")
def view_index():
    return render_template('index.html', user=None)


@app.route('/about/')
def view_about():
    return render_template('about.html', user=None)


@app.route('/launcher/')
def view_launcher():
    return render_template('launcher.html', user=None)


@app.route('/login/')
@app.route('/logout/')
@app.route('/monitor/')
@app.route('/nodes/')
@app.route('/nodes/<server_id>')
@app.route('/register/')
@app.route('/runlog/<int:run_id>/')
def xmeow():
    return "<i><b>COMING SOON!</b></i>"

#############################################################################
# App entry points for plug-ins

if __name__ == "__main__":
    print '\nPSRC QUEUE'
    plugins.register_plugins(app)
    app.run()
