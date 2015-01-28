from __future__ import print_function
import Pyro4

server_hostname = '192.168.56.1'

class Jobs(object):
    def __init__(self):
        self.jobs = []
        self.test = 'here is a test'

    def add_job(self, job):
        self.jobs.append(job)
        print("Job: {0} added to the queue.".format(job))

def main():
    jobs = Jobs()
    Pyro4.Daemon.serveSimple(
                             {
                                jobs: "example.jobs"
                             },
                             host = server_hostname,
                             ns = True)

if __name__=="__main__":
    main()