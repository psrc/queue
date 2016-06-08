import plugins
from server import app

print '\nPSRC QUEUE'
plugins.register_plugins(app)
app.run()
