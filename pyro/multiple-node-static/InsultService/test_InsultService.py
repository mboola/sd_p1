import time
import sys
from loadBalancerInsultService import RoundRobinBalancerInsult
from client import ClientInsult


def main():
    n_is = int(sys.argv[1]) # Numero de InsultService
    n_if = int(sys.argv[2]) # Numero de InsultFilterService
    n_pis = int(sys.argv[3])  # Numero de peticiones de insultos
    n_pif = int(sys.argv[4])  # Numero de peticiones de textos

    balancer = RoundRobinBalancerInsult("InsultService_")
    client = ClientInsult(balancer)

    print(f" ENVIANDO {n_pis} insultos a través del balanceador RoundRobin...")
    start = time.time()
    client.send_insult(n_pis)
    end = time.time()

    total_time = end - start
    throughput = n_pis / total_time

    results = (
        f"TEST MODULAR: InsultService (RoundRobin)\n"
        f"Total instancias: {balancer.total}\n"
        f"Total peticiones: {n_pis}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(results)
    with open(f"resultados_scaling_insultservice_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
