import Pyro4

name_server = Pyro4.locateNS()
uri = name_server.lookup("example.remote.object")
remote_object_subject = Pyro4.Proxy(uri)

print(remote_object_subject.greet("Massin"))
print(remote_object_subject.add(1,1))
print("Métodos disponibles en el objeto remoto:", remote_object_subject._pyroMethods)