model-dashboard
===============

This code allows a user to start and manage travel model runs on PSRC's internal servers. The repo includes a webpage application to access and initiate runs in the "dashboard" directory. A simple sever-side script (client.py) is also included in the main directory. This script must be actively running on a modelsrv machine before the server will accept model run requests from the web app.

The web-app engine is Python-based Django. 

To get the web application up and running:
- clone the repo
- cd to "dashboard" directory and run the following in the shell: **python manage.py runserver 0.0.0.0:8000**. This will host the app on the local network. 
- Other machines on the network can access the app page through http://a.b.c.d:8000/controller, where a, b, c, and d are the components of the LAN IPv4 address. Depending on where this app is hosted, this will be a fixed location in implementation. (It will also have to be hosted on an external network at some point.) Look up your ipv4 with "ipconfig" in the shell.

To set up servers for running Soundcast on demand from the web app:
- download "client.py" to a directory where we want model runs stored
- run client.py from the shell: "python client.py"
- this sets up a communication port on the modelsrv machine, waiting patiently for a command from the web-app


