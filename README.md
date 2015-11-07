PSRC Queue
===============

PSRC Queue is a modeling meta platform. That means you plug your own model into it — any model will do — and Queue allows you to set up, start, and manage your model runs. It can spawn runs on your local network servers, and soon will work seamlessly with EC2 and other cloud resources. All model inputs are archived using Git and Git Fat, to ensure trivial reproducibility of any past model run. 

Queue includes a web application to centrally launch manage model runs, and a simple script for worker nodes that allows those nodes to listen for job requests and do Queue's bidding. If you're accustomed to running models locally from a black box command window, you can still do that too: your run details can get pushed to Queue's central database so everything can be tracked whether you use the web interface or not.

Fully buzzword-enabled:
* Queue's web-app front end is Python-based Django. 
* The inter-machine communication uses Python Remote Objects, Pyro4. 
* Git and specifically git-fat for archiving model inputs, even including large files

We would love your contributions in code or ideas to make Queue bulletproof and more feature-rich. 

