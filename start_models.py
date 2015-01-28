# This runs the example code
import sys
import Pyro4
import Pyro4.util


class ModelRun(object):
    def __init__(self, name):
        self.name = name

    def add_job(self, joblist):
        joblist.add_job(self.name)
        
def main():
    sys.excepthook = Pyro4.util.excepthook

    joblist = Pyro4.Proxy("PYRONAME:example.jobs")

    # Create a new job and add it to the queue
    newrun = ModelRun("Soundcast 2040")     # Start an instance of a new model run
    newrun.add_job(joblist)                 # Add this job to the job queue

if __name__=="__main__":
    main()
