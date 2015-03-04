model-dashboard
===============

This code allows a user to start and manage travel model runs on PSRC's internal servers. The repo includes a webpage application to access and initiate runs in the "dashboard" directory. A simple sever-side script (client.py) is also included in the main directory. This script must be actively running on a modelsrv machine before the server will accept model run requests from the web app.

The web-app engine is Python-based Django. 

To get the web application up and running:

- clone the repo
- cd to "dashboard" directory and run the following in the shell: python manage.py runserver


