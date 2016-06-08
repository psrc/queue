from server import app, plugins

print '\nPSRC QUEUE'
plugins.register_plugins(app)
app.run()
