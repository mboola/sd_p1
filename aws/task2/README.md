# Task 2 - Operación de flujo dinámica

En esta carpeta se implementa una operación de *stream* que permite procesar mensajes de una cola en SQS lanzando instancias de una función de manera dinámica.

### Objetivo
La operación recibe los parámetros `(funcion, maxfunc, queue)` y se encarga de:
1. Crear hasta `maxfunc` instancias concurrentes de la función indicada.
2. Procesar los mensajes presentes en la cola especificada.
3. Aumentar o reducir el número de workers según la carga de la cola.

Esta tarea reutiliza código de la tarea 1 y demuestra un escalado automático basado en el número de mensajes pendientes.