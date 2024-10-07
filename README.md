El programa simula y genera una instancia real con distintos parámetros necesarios para optimizar los horarios de clase respectivos.
Una vez generada la instancia se procede a generar un archivo .lp ejecutable con con el software lp_solve en consola.

Iniciar el programa:
python3 instancias.py --grande --mediano --chico

Las banderas hacen referencia a la magnitud/tamaño de la instancia creada. Si seleccionamos todas se crean en las 3 magnitudes distintas, pero podemos crear las que nos sean necesarias.

Ejecutar la optimización:
lp_solve model_{tamaño}.lp -ia 

-ia es para únicamente mostrar las variables que son distintas de cero.

Para esto debemos tener instalado el programa lp_solve en la consola de linux.