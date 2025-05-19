import random
import uuid

class ClientFilter:
    def __init__(self, balancer):
        self.balancer = balancer

    def send_text(self, N):
        for i in range(N):
            text = f"{i + random.randint(1, N)} {str(uuid.uuid4())} Este texto contiene insulto_{i}"
            self.balancer.send(text)
