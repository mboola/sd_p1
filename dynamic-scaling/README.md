## Services

- `InsultService`: Emits insults and handles unique insult storage.
- `InsultFilterService`: Censors insults in text data.
- `Notifier`: Manages periodic broadcast of insults to subscribers.

## How to run:

1. Launch `docker-compose-rabbitmq.yml`.
2. Start Redis.
3. Run `autoscaler.py` to initiate the dynamic scaling system.