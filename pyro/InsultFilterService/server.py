import Pyro4

@Pyro4.behavior(instance_mode="single")
class InsultFilterService:
    def __init__(self):
        self.insults_list = ["idiota", "imbécil", "estúpido", "inútil", "cretino", "payaso", "baboso",
        "zángano", "burro", "animal", "bestia", "analfabeto", "cabrón", "capullo",
        "subnormal", "gilipollas", "pelotudo", "boludo", "tarado", "bobo",
        "estúpida", "idiota", "imbécila", "babosa", "loca", "locazo", "zorra",
        "perra", "malparido", "malnacido", "huevón", "pendejo", "mongólico",
        "retrasado", "atontado", "patán", "necio", "tonto", "ganso", "imbécilazo",
        "choto", "cara de culo", "cara de mierda", "asqueroso", "repugnante",
        "mierda", "basura", "escoria", "muerto de hambre", "pelmazo", "metepatas",
        "desgraciado", "maldito", "idiotizado", "cretina", "mierdoso", "pelotuda",
        "boluda", "gila", "zorra", "infeliz", "payasa", "chiflado", "mamerto",
        "mamón", "baboso", "capulla", "lameculos", "chupamedias", "soplapollas",
        "come mierda", "come mocos", "tarambana", "tarugo", "majadero", "chingaquedito"]  # Insultos a filtrar
        self.filtered_texts = [] # Resultados filtrados
        self.subscribers = []  # Lista de URLs de suscriptores

    @Pyro4.expose
    def add_text(self, string):
        text_filtered = self.filter_text(string)
        if text_filtered not in self.filtered_texts:
            self.filtered_texts.append(text_filtered)
            return "Texto registrado: " + text_filtered
        else:
            return "Cadena ya se encontraba registrada"

    def filter_text(self, text):
        if (text not in self.insults_list):
            return text
        else: 
            return "CENSORED"
    
    @Pyro4.expose
    def get_texts(self):
        return self.filtered_texts

def main():
    daemon = Pyro4.Daemon(port=4040)
    obj = InsultFilterService()
    uri = daemon.register(obj, objectId="InsultFilterService")
    print(f"InsultFilterService with URI: {uri} in execution...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()