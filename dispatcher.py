import Pyro4, time

# experimental
proxy=Pyro4.core.Proxy("PYRONAME:test")
proxy.runmodel()


#thing = Pyro4.Proxy("PYRONAME:mythingy")
#thing.runmodel()

# Access the object run on the client machines
# Below code works fine
#uri_string = "PYRO:test@psrc3827:54277"
#testserver = Pyro4.Proxy(uri_string)
#testserver.runmodel()