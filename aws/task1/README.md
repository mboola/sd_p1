# Task 1 - InsultFilter en la nube

Este directorio contiene la implementación de la primera tarea de AWS. El objetivo es portar el servicio **InsultFilter** a la nube utilizando una cola en RabbitMQ y ejecutar los trabajadores como funciones **Lambda** que escalan de forma dinámica, reutilizando y adaptando el dynamic-scaling de la practica-1.

### Objetivo
1. Enviar textos con o sin insultos a una cola en la nube (RabbitMQ).
2. Lanzar funciones Lambda que actúan como *workers* para procesar los mensajes.
3. Escalar dinámicamente el número de workers según la carga de la cola.

Para demostrar la escalabilidad se utilizan llamadas asíncronas de Lithops o las APIs de AWS.

### Archivos relevantes
- `lambda_order_publisher.py`: publica textos en la cola.
- `lambda_filter_service.py`: función Lambda que filtra insultos.
- `autoscaler.py`: orquesta la ejecución y escalado de las funciones.

Además se incluyen scripts y gráficas de prueba en el directorio `graphs/`.

### Command to transfer files from AWS
scp -i "sdlabkeys.pem" -r admin@ec2-100-24-67-23.compute-1.amazonaws.com:. AWS/final_p1