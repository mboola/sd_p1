# Comparison of Middleware in Scalable Distributed Services

This project aims to design, implement, and analyze the performance of scalable distributed services using different communication middleware: XMLRPC, PyRO, Redis, and RabbitMQ. The goal is both the functional implementation of the services and a comparative study of their behavior under different load and scalability conditions.

The developed services are:

- **InsultService:** a service that allows receiving insults remotely, storing them only if they are not repeated, and retrieving them later. It also implements a periodic event broadcasting system that publishes random insults every five seconds.

- **InsultFilter:** a service based on the Work Queue pattern, which receives texts and replaces insults with the word "CENSORED", storing the filtered results. It also allows retrieval of the set of processed texts.

Both services must be implemented using the four aforementioned technologies, and their correct operation must be demonstrated through test scripts or unit tests.

Subsequently, a performance analysis is required under three different scenarios:

- *Analysis on a single node*, measuring the processing capacity of each implementation.

- *Static scaling across multiple nodes*, testing configurations with one, two, and three nodes, and calculating the speedups obtained.

- *Dynamic scaling*, designing an architecture that automatically adapts the number of nodes based on the workload, using metrics such as message arrival rate, average processing time, and backlog.

Finally, the design and architecture of each solution must be documented, including the experimental results with their respective graphs and comparative analysis.


## Project Overview

This project implements a distributed insult management system using:

- RabbitMQ as a messaging middleware
- Redis as a fast in-memory database
- PyRO for remote object communication between services
- Plotly Dash for a real-time monitoring dashboard

The system is designed to be scalable, modular, and resilient to failures. It supports:

- Dynamic scaling of microservices based on message queue load
- Asynchronous communication between clients and services
- Real-time processing and filtering of text data
- Broadcasting of random insults to subscribers
- Visualization of system metrics in a live dashboard

Clients send:

- Insults → pushed to a queue and consumed by `InsultService` nodes

- Texts → pushed to a separate queue and filtered by `InsultFilterService` nodes

The system scales up/down `InsultService` and `InsultFilterService` instances based on RabbitMQ queue size.


### How to run:
- [XML-RPC]()
- [PyRO](./pyro/README.md)
- [Redis]()
- [RabbitMQ](./rabbitmq/README.md)
- [Dynamic-scaling](./dynamic-scaling/README.md)


### Folder Structure

````
.
├── dynamic-scaling/           # Dynamic autoscaling architecture and services
│   ├── InsultService/         # InsultService with notifier and tests
│   ├── InsultFilterService/   # InsultFilterService with tests
│   └── Notifier/              # Publisher-subscriber implementation
│
├── pyro/                      # PyRO implementation
│   ├── single-node/           # Single node execution setup
│   └── multiple-node-static/  # Static scaling on n nodes
│
├── rabbitmq/                  # RabbitMQ implementation
│   ├── single-node/           # Single node execution setup
│   └── multiple-node-static/  # Static scaling on n nodes
│
├── resources/img/             
├── requirements.txt           
└── README.md                  

````
<br>

## Member's
- **[Marcel Povill](https://github.com/mboola)**
- **[Massin Laa.](https://github.com/massinlaaouaj)**

