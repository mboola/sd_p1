import random

class ClientFilter:
    def __init__(self, balancer):
        self.balancer = balancer

    def send_text(self, N):
        for i in range(N):
            text = f"{random.randint(1, 100)} Este texto contiene insulto_{i}"
            self.balancer.send(text)
