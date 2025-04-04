import Pyro4

name_server = Pyro4.locateNS()
uri = name_server.lookup("insultservice.remote.object")
remote_object_subject = Pyro4.Proxy(uri)

print(remote_object_subject.add_insult("Asshole"))
print("\n\nMétodos disponibles en el objeto remoto:", remote_object_subject._pyroMethods)