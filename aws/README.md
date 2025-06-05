# Overview

Este directorio contiene las cuatro tareas desarrolladas para desplegar y escalar el servicio **InsultFilter** en AWS. Cada subcarpeta incluye el código correspondiente a una de las tareas.

## Task1 - InsultFilter en la nube
Portar el servicio a la nube enviando textos a una cola (RabbitMQ o SQS) y procesándolos con funciones **Lambda** que escalan dinámicamente.

## Task2 - Operación de *stream*
Implementar una operación `stream(function, maxfunc, queue)` que lanza hasta `maxfunc` instancias de la función para procesar los mensajes de la cola, escalando automáticamente según la carga.

## Task3 - Filtrado con Lithops
Utilizar `Lithops` con `map` y `reduce` para censurar insultos en archivos almacenados en un bucket de S3. Los resultados censurados se guardan en el bucket y se suma el total de insultos censurados.

## Task4 - Operación *batch*
Crear una operación `batch(function, maxfunc, bucket)` que ejecuta hasta `maxfunc` funciones concurrentes para procesar los archivos de un bucket, limitando así el número de ejecuciones simultáneas. Se verifica repitiendo la Task3 con un valor de `maxfunc` menor al número de archivos.