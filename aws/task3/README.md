# Task 3 - Filtrado de insultos con Lithops

Esta tarea emplea Lithops para paralelizar el filtrado de insultos sobre un conjunto de archivos de texto almacenados en un bucket de S3.

### Pasos principales
1. Se utiliza `map` para ejecutar el filtrado de cada archivo de manera distribuida.
2. Con `reduce` se recopilan los resultados y se contabiliza el total de insultos censurados.
3. Los archivos censurados se guardan de nuevo en el bucket de origen.

El script `filter_starter.py` muestra cómo lanzar el proceso y registrar el número de insultos encontrados.