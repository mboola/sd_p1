import Pyro4
import random

def main():
    ns = Pyro4.locateNS()
    insult_filter_service_server_uri = ns.lookup("InsultFilterService")
    print("Conectando al InsultFilterService...")
    insult_filter_service_server = Pyro4.Proxy(insult_filter_service_server_uri)

    texts = [
        "Realmente eres un stupid", "Si no hay mas", "Eres un jerk", "En la madrugada habia un dumbass as clown que no paraba de molestar", "Esto lo puede hacer hasta un loser piensalo bien", "Sin un idiot no podemos continuar ya que los idiot son importantes"
    ]

    def get_random_text():
        insult = random.choice(texts)
        print("Texto a filtrar:", insult)
        return insult

    text = "Realmente eres un stupid"
    print("Texto a filtrar:", get_random_text())
    if text:    
        result = insult_filter_service_server.add_text(text)
        print("📤 Resultado:", result)


if __name__ == "__main__":
    main()
