def crea_combinaciones(instancia):
    #Primeramente necesitamos una función que nos haga la combinación de todas las formas posibles, es decir, 
    # (a,s,b,d) Asignatura, sala, bloque, dia
    combinaciones = {}
    for asignatura in instancia['asignaturas']:
        for sala in instancia['salas']:
            for bloque in instancia['bloques']:
                for dia in instancia['dias']:
                    if asignatura  not in combinaciones:
                       combinaciones[asignatura] = []
                       combinaciones[asignatura].append( [sala, bloque,dia] )
                    else:
                        combinaciones[asignatura].append( [sala, bloque,dia] )
    return combinaciones

#Recibe como parametro una única instancia
def crea_modelo(instancia, nombre_archivo):
    combinaciones_por_asignatura = crea_combinaciones(instancia)
    # print(combinaciones)

    # Crea archivo
    archivo = open(nombre_archivo+'.lp', 'w')
    # Escribe el contenido en el archivo
    funcion_objetivo = 'max: '
    bn = 'bin '
    res1 = '' #restricción sumatoria de las combinaciones para una asignatura particular debe sumar menor igual a 1
    res2 = '' #restricción horarios que no pueden asistir los profesores de det asignatura
    res3 = '' #restricción cantidad de bloques por semana
    for key in combinaciones_por_asignatura:
        
        priority = instancia['asignaturas'][key]['prioridad'] # Rescata la prioridad de la asignatura
        bloques_semanales = instancia['asignaturas'][key]['cantidad_bloques'] # Rescata la cantidad de bloques semanales x asignatura
        
        temp = ''

        # Recorriendo todas las combinaciones posibles para una asignatura particular. c = [sala,bloque,dia] ejemplo
        for c in combinaciones_por_asignatura[key]:
            y_particular = f'y{key}.{c[0]}.{c[1]}.{c[2]}' # y(asignatura).(sala).(bloque).(dia) [todas las comb posibles]
            funcion_objetivo += f' { priority } {y_particular} +'

            temp+= y_particular+' +' # Sumatoria de todas las combinaciones para una asignatura particular (Creando restricción inicial)

            # Verifica si el profesor tiene el bloque disponible sin importar la sala, si no está disponible, restringe esa combi
            if tuple(c[1:]) in instancia['asignaturas'][key]['bloques_no_disponibles']:
                res2+= f'{y_particular} = 0;\n'
            else:
                # Ya que los limites se deben definir solo 1 vez
                bn += f'{y_particular},' # Esta cadena es para definirlas todas como variables binarias luego
                
        
        # Agrega la restricción de que la sumatoria de las combinaciones para una asignatura particular debe sumar menor igual a 1
        temp = temp[:-1]
        # res1+= f'{temp}<= 1;\n'
        res3+= f'{temp} = {bloques_semanales};\n'

    # Esto solamente lo hago para evitar el problema de que me quede el signo más al final, no se me ocurrio una idea más pulcra
    funcion_objetivo = funcion_objetivo[:-1]
    funcion_objetivo += ';'
    # Usamos el comando bin para denotar que son variables binarias
    bn = bn[:-1]
    bn += ';'

    archivo.write( funcion_objetivo+'\n\n')
    # Ahora la idea seria encajar la primera reestricción, por ejemplo:
    # y1.1.1.1 + y1.1.1.2 + y1.1.1.3 +  y1.1.1.4 \leq 1
    # Suponiendo que en este caso que solo hay 4 dias y 1 bloque y una sala. 
    #Es decir, todas las combinaciones siguinetes para una asignatura particular
    #Solo una combinacion puede ser correcta.
    
    archivo.write( res1 )
    archivo.write( res2 )
    archivo.write( bn )

    print(f'Archivo {nombre_archivo}.lp creado.')

    # Cierra el archivo para asegurarte de que se guarde correctamente
    archivo.close()
