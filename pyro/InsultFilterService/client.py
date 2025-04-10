from Pyro4 import Proxy

# Conectar con el servidor
remote = Proxy("PYRO:InsultFilterService@localhost:4040")

# Enviar texto a filtrar
text = "hola"
filtered = remote.add_text(text)
print("Texto filtrado:", filtered)

# Obtener todos los resultados filtrados
results = remote.get_texts()
print("Lista de textos filtrados:", results)