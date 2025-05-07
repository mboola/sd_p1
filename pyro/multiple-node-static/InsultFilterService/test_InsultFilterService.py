import time
import sys
from loadBalancerInsultFilterService import RoundRobinBalancerFilter
from client import ClientFilter

def main():
    n_is = int(sys.argv[1]) # Numero de InsultService
    n_if = int(sys.argv[2]) # Numero de InsultFilterService
    n_pis = int(sys.argv[3])  # Numero de peticiones de insultos
    n_pif = int(sys.argv[4])  # Numero de peticiones de textos

    balancer = RoundRobinBalancerFilter("InsultFilterService_")
    client = ClientFilter(balancer)

    print(f" ENVIANDO {n_pif} textos a través del balanceador RoundRobin...")
    start = time.time()
    client.send_text(n_pif)
    end = time.time()

    total_time = end - start
    throughput = n_pif / total_time

    results = (
        f"TEST MODULAR: InsultFilterService (RoundRobin)\n"
        f"Total instancias: {balancer.total}\n"
        f"Total peticiones: {n_pif}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(results)
    with open(f"resultados_scaling_insultfilterservice_{n_is}_{n_if}_{n_pis}_{n_pif}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
