import Pyro4
import time
import sys

def main():
    n_pif = int(sys.argv[1])
    logfile = f"resultados_insultfilterservice_{n_pif}_pyro.txt"

    ns = Pyro4.locateNS()
    insult_filter_service_server_uri = ns.lookup("InsultFilterService")
    insult_filter_server = Pyro4.Proxy(insult_filter_service_server_uri)

    print(f" Enviando {n_pif} textos al servicio InsultFilterService (Pyro4)...")

    start = time.time()
    for i in range(n_pif):
        texto = f"{i} este texto contiene insulto_{i}"
        insult_filter_server.add_text(texto)
    end = time.time()

    total_time = end - start
    throughput = n_pif / total_time

    output = (
        f"TEST: InsultFilterService (Pyro4)\n"
        f"Total requests: {n_pif}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput: {throughput:.2f} peticiones/segundo\n"
    )

    print(output)
    with open(logfile, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
