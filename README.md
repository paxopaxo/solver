El programa simula y genera una instancia real con distintos parámetros necesarios para optimizar los horarios de clase respectivos.
Una vez generada la instancia se procede a generar un archivo .lp ejecutable con con el software lp_solve en consola.

Iniciar el programa:
python3 instancias.py

Ejecutar la optimización:
lp_solve -S3 model.lp

Para esto debemos tener instalado el programa lp_solve en la consola de linux.