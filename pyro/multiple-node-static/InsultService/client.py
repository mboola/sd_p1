class ClientInsult:
    def __init__(self, balancer):
        self.balancer = balancer

    def send_insult(self, N):
        for i in range(N):
            insulto = f"insulto_{i}"
            self.balancer.send(insulto)