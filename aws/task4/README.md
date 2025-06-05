# Task 4 - Operación batch con límite de concurrencia

La cuarta tarea amplía el filtrado anterior implementando una operación de *batch* con los parámetros `(funcion, maxfunc, bucket)`.

### Descripción
- Se lanzan hasta `maxfunc` ejecuciones concurrentes de la función indicada para procesar los archivos de un bucket de S3.
- A diferencia de `Lithops.map`, esta operación impone un tope al número de funciones activas al mismo tiempo.
- Para verificar su funcionamiento se repite el ejercicio 3 estableciendo `maxfunc` a un valor menor que el total de archivos disponibles.

El código de ejemplo en `filter_starter.py` muestra cómo iniciar el proceso utilizando esta operación batch.