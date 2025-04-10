from Pyro4 import Proxy

remote = Proxy("PYRO:InsultService@localhost:4718")

def test_add_insult():
    result = remote.add_insult("idiota")
    assert result == "Insulto registrado: idiota" or result == "Insulto ya registrado"
    print("OK")

def test_no_duplicates():
    remote.add_insult("idiota")
    result = remote.add_insult("idiota")
    assert result == "Insulto ya registrado"
    print("OK")

def test_get_insults():
    insults = remote.get_insults()
    assert isinstance(insults, list)
    assert "idiota" in insults
    print("OK")

test_add_insult()
test_no_duplicates()
test_get_insults()
