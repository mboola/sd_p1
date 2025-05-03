import Pyro4
import time

N = 1000
LOGFILE = f"resultados_insultfilterservice_{N}_pyro.txt"

def main():
    ns = Pyro4.locateNS()
    insult_filter_service_server_uri = ns.lookup("InsultFilterService")
    insult_filter_server = Pyro4.Proxy(insult_filter_service_server_uri)

    print(f" Enviando {N} textos al servicio InsultFilterService (Pyro4)...")

    start = time.time()
    for i in range(N):
        texto = f"este texto contiene insulto_{i}"
        insult_filter_server.add_text(texto)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    output = (
        f"TEST: InsultFilterService (Pyro4)\n"
        f"Total requests: {N}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput: {throughput:.2f} peticiones/segundo\n"
    )

    print(output)
    with open(LOGFILE, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
