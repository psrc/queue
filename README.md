PSRC Queue
===============

PSRC Queue is a modeling "meta" platform. That means you plug your own model into it — any model will do — and Queue allows you to set up, start, and manage your model runs. It can spawn runs on your local network servers, and soon will work seamlessly with EC2 and other cloud resources. All model inputs are archived using Git and Git Fat, to ensure trivial reproducibility of any past model run. 

Queue includes a web app to centrally launch and manage model runs, and a simple script for worker nodes that allows those nodes to listen for job requests and do Queue's bidding. If you're accustomed to running models locally from a black box command window, you can still do that too: your run details can get pushed to Queue's central database so everything can be tracked whether you use the web interface or not.

Fully buzzword-enabled:
* Queue's web-app front end is Python-based [Django](https://www.djangoproject.com/). 
* The inter-machine communication uses Python Remote Objects, [Pyro4](https://pythonhosted.org/Pyro4/). 
* Git and specifically [git-fat](https://github.com/jedbrown/git-fat) for archiving all model inputs, even supporting large files

*We need your love and your contributions (in code or ideas) to make Queue bulletproof and more feature-rich.*

**OK I'm in!** Take me to the [PSRC Queue documentation](https://github.com/psrc/queue/wiki).
