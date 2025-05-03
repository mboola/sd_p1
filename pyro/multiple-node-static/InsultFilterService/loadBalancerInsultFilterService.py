import Pyro4

class RoundRobinBalancerFilter:
    def __init__(self, prefix_service):
        ns = Pyro4.locateNS()
        services = sorted(ns.list(prefix=prefix_service).keys())
        if not services:
            raise Exception("No se encontraron servicios con ese prefijo.")
        self.proxies = [Pyro4.Proxy(ns.lookup(name)) for name in services]
        self.total = len(self.proxies)
        self.i = 0

    def send(self, text):
        proxy = self.proxies[self.i]
        self.i = (self.i + 1) % self.total
        proxy.add_text(text)
