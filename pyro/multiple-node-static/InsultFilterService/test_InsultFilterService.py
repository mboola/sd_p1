import time
from loadBalancerInsultFilterService import RoundRobinBalancerFilter
from client import ClientFilter

N = 1000

def main():
    balancer = RoundRobinBalancerFilter("InsultFilterService_")
    client = ClientFilter(balancer)

    print(f" ENVIANDO {N} textos a través del balanceador RoundRobin...")
    start = time.time()
    client.send_text(N)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    results = (
        f"TEST MODULAR: InsultFilterService (RoundRobin)\n"
        f"Total instancias: {balancer.total}\n"
        f"Total peticiones: {N}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(results)
    with open(f"resultados_scaling_insultfilterservice_{N}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
