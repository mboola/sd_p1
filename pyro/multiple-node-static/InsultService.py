import Pyro4
from InsultStorage import InsultStorage

class InsultService:
    def __init__(self, insults):
        self.insults = insults         # Lista compartida de insultos
        self.insults_storage = InsultStorage(insults).get_insults()

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
        else:
            return "Insulto ya registrado"
        return "Insulto registrado: " + insult