PSRC Queue
===============

PSRC Queue is a modeling "meta" platform. That means you plug your own model into it — any model will do — and Queue allows you to set up, start, and manage your model runs. 

Queue can spawn long-running models on your local network servers, and will email you when the run dies or completes successfully. Soon, Queue will eventually work seamlessly with EC2 and other cloud resources.

All model inputs are archived to ensure trivial reproducibility of any past model run. If your model auto-generates summary stats or visualizations, those can be linked directly and viewed from the Queue dashboard.

Queue includes a web app to centrally launch and manage model runs, and a simple script for worker nodes that allows those nodes to listen for job requests and do Queue's bidding. If you're accustomed to running models locally from a black box command window, you can still do that too: your run details can get pushed to Queue's central database so everything can be tracked whether you use the web interface or not.

Fully buzzword-enabled:

* Queue's web-app front end is Python-based [Flask](http://flask.pocoo.org/).
* The inter-machine communication uses REST and Python Remote Objects, [Pyro4](https://pythonhosted.org/Pyro4/).
* Git and [Borg Backup](https://borgbackup.readthedocs.io/en/stable/) for archiving all model inputs, even supporting deduplication of large files

*We need your love and your contributions (in code or ideas) to make Queue bulletproof and more feature-rich.*

**OK I'm in!** Take me to the [PSRC Queue documentation](https://github.com/psrc/queue/wiki).
