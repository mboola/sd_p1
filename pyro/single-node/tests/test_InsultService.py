import Pyro4
import time
import sys

def main():
    n_pis = int(sys.argv[1])
    logfile = f"resultados_insultservice_{n_pis}_pyro.txt"
    
    ns = Pyro4.locateNS()
    insult_service_server_uri = ns.lookup("InsultService")
    insult_service_server = Pyro4.Proxy(insult_service_server_uri)

    print(f" Enviando {n_pis} insultos al servicio InsultService (Pyro4)...")

    start = time.time()
    for i in range(n_pis):
        insult = f"insulto_{i}"
        insult_service_server.add_insult(insult)
    end = time.time()

    total_time = end - start
    throughput = n_pis / total_time

    output = (
        f"TEST: InsultService (Pyro4)\n"
        f"Total requests: {n_pis}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput: {throughput:.2f} peticiones/segundo\n"
    )

    print(output)
    with open(logfile, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
