import random
import math
import json
import solver

def guardar_diccionario_como_json(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo_json:
        json.dump(diccionario, archivo_json, indent=4, ensure_ascii=False, separators=(',', ': '))
    print(f"Archivo '{nombre_archivo}' creado con éxito.")


#Generador de instancias:

#Primero creamos la funcion que nos devuelve las instancias, donde definimos las parametros y las restricciones:

def generar_instancia(num_asignaturas, num_salas, b):
    
    A = list(range(1, num_asignaturas + 1))      
    S = list(range(1, num_salas + 1))        
    B = list(range(1, 15))                   
    D = list(range(1, 6))                    

    # La cantidad de elementos que forman el 65% del total de las asignaturas 
    n = math.floor( len(A)*0.65 ) 
    # Selecciono un muestreo aleatorio de A de n elementos 
    bloques_true = random.sample(A, n)

    # Diccionario donde se especifica si necesitan 1 o 2 bloques semanales segun la asignatura
    asignaturas = {}

    # Asignar True o False según si está en bloques_true
    for i in A:
        if i in bloques_true:
            asignaturas[i] = {'cantidad_bloques': 1}
        else:
            asignaturas[i] = {'cantidad_bloques': 2}

    # print(bloques_semanales)
    
    ########################################
    # Idea anterior....
    ########################################
    # bloques_semanales = {}
    # for i in A:
    #     if random.random() <= 0.65:
    #         bloques_semanales[i] = 1
    #     else:
    #         bloques_semanales[i] = 2
    ########################################
    ########################################

    
    for i in A:
        num_bloques_no_disponibles = random.randint(7, 21)
        asignaturas[i]['bloques_no_disponibles'] = random.sample([(k, h) for k in B for h in D], num_bloques_no_disponibles)
    
    # Por cada 5 asignaturas hay 1 indispensable, por tanto el 20% de las asignaturas son indispensables
    n_indispensable = math.floor( len(A)*0.2 ) 
    n_no_indispensable = math.floor( len(A) ) - n_indispensable

    #Creo un arreglo con valores aleatorios que cumplen la proporcion mencionada al principio, en este se almacenan todas las prioridades
    prioridades = []
    for _ in range(n_indispensable):
        # Le asigna una prioridad al azar sabiendo que es indispensable
        prioridad = random.randint(6,10)
        prioridades.append( prioridad )
    for _ in range(n_no_indispensable):
        # Mismo caso
        prioridad = random.randint(1,5)
        prioridades.append( prioridad )

    # desordeno aun mas el arreglo
    random.shuffle(prioridades)


    # instancia = {
    #     "asignaturas": A,
    #     "salas": S,
    #     "bloques_semanales": bloques_semanales,
    #     "horarios_no_disponibles": horarios_no_disponibles
    # }

    salas_dics = {}
    for i in S:
        salas_dics[i] = {'capacidad' : random.randint(45,80), 'horarios': [(k, h) for k in B for h in D] }

    #Aqui simplemente lo estoy mapeando a la estructura original que habiamos creado
    # recordar que A son los valores del 1 al n, cuando lo recorremos resto 1 para evitar que este fuera de rango con 
    # prioridades donde su indice parte del cero.
    for i in A:
        asignaturas[i]['prioridad'] = prioridades[i-1]
        asignaturas[i]['salas'] = salas_dics
    
    instancia = {
        "asignaturas": asignaturas,
        "salas": salas_dics,
        "bloques": B,
        "dias": D
    }
    return instancia

#Generador de instancias pequeñas
def generar_instancias_pequenas(num_instancias):
    instancias = []
    num_salas = 1 #Siempre sera una sala en esta instancia (según el proyecto) 
    for _ in range(num_instancias):
        num_asignaturas = random.randint(10, 50) #? Que los genere hasta ahi por ahora
        instancia = generar_instancia(num_asignaturas, num_salas, b=1)
        instancias.append(instancia)
    return instancias

#Generador de instancias medianas y grandes
def generar_instancias_medianas_grandes(tipo='mediana', num_instancias=5):
    instancias = []
    #La tabla segun B=1 es:
    if tipo == 'mediana':
        asignaturas_rangos = [(40, 45), (54, 58), (68, 72), (80, 85), (95, 99)]
        salas_rangos = [3, 4, 5, 6, 7]  
    elif tipo == 'grande':
        asignaturas_rangos = [(180, 200), (210, 230), (250, 270), (300, 320), (340, 360)]
        salas_rangos = [(9, 11), (12, 14), (15, 17), (18, 20), (21, 23)]  

    for _ in range(num_instancias):
        asignaturas_rng = random.choice(asignaturas_rangos)
        num_asignaturas = random.randint(asignaturas_rng[0], asignaturas_rng[1])

        if tipo == 'mediana':
            num_salas = random.choice(salas_rangos)
        elif tipo == 'grande':
            salas_rng = random.choice(salas_rangos)
            num_salas = random.randint(salas_rng[0], salas_rng[1])

        instancia = generar_instancia(num_asignaturas, num_salas, b=1)
        instancias.append(instancia)

    return instancias

# Print de 5 instancias en cada caso (pequeña, mediana y grande)
# print("Generando instancias pequeñas...")
# instancias_pequenas = generar_instancias_pequenas(1)
# guardar_diccionario_como_json(instancias_pequenas, 'instancias_pequenas')
# for i, instancia in enumerate(instancias_pequenas, 1):
#     print(f"Instancia pequeña {i}: {instancia}")

print("\nGenerando instancias medianas...")
instancias_medianas = generar_instancias_medianas_grandes(tipo='mediana', num_instancias=1)
guardar_diccionario_como_json(instancias_medianas, 'instancias_medianas')

# for i, instancia in enumerate(instancias_medianas, 1):
#     print(f"Instancia mediana {i}: {instancia}")

# print("\nGenerando instancias grandes...")
# instancias_grandes = generar_instancias_medianas_grandes(tipo='grande', num_instancias=5)
# guardar_diccionario_como_json(instancias_grandes, 'instancias_grandes')

# for i, instancia in enumerate(instancias_grandes, 1):
#     print(f"Instancia grande {i}: {instancia}")

solver.crea_modelo(instancias_medianas[0], 'model_mediana')
# solver.crea_modelo(instancias_pequenas[0], 'model_pequena')