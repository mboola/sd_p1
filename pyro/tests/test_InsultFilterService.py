from Pyro4 import Proxy

remote = Proxy("PYRO:InsultFilterService@localhost:4040")

def test_filter_text():
    text = "idiota"
    filtered = remote.filter_text(text)
    assert "CENSORED" in filtered
    assert "idiot" not in filtered
    print("OK")

def test_get_results():
    results = remote.get_results()
    assert isinstance(results, list)
    assert any("CENSORED" in r for r in results)
    print("OK")

test_filter_text()
test_get_results()
