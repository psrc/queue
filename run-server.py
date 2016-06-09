import os
import plugins
from server import app, manager

EXTRA_WATCH_DIRS = ['server/templates/']

print '\nPSRC QUEUE'
plugins.register_plugins(app)

# Flask doesn't watch template files in debug mode
extra_files = EXTRA_WATCH_DIRS[:]
for extra_dir in EXTRA_WATCH_DIRS:
    print 'Watching extra dir for changes:', extra_dir
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

print extra_files

# manager.run()
app.run(debug=True, extra_files=extra_files)

