import time
from loadBalancerInsultService import RoundRobinBalancerInsult
from client import ClientInsult

N = 1000

def main():
    balancer = RoundRobinBalancerInsult("InsultService_")
    client = ClientInsult(balancer)

    print(f" ENVIANDO {N} insultos a través del balanceador RoundRobin...")
    start = time.time()
    client.send_insult(N)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    results = (
        f"TEST MODULAR: InsultService (RoundRobin)\n"
        f"Total instancias: {balancer.total}\n"
        f"Total peticiones: {N}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(results)
    with open(f"resultados_scaling_insultservice_{N}.txt", "w") as f:
        f.write(results)

if __name__ == "__main__":
    main()
