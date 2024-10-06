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

    # Crea archivo
    archivo = open(nombre_archivo+'.lp', 'w')
    # Escribe el contenido en el archivo
    funcion_objetivo = 'max: '
    bn = 'bin '
    res1 = '' #restricción Cada asignatura solo puede usar \textbf{una} sala en un determinado bloque y día.
    res2 = '' #restricción horarios que no pueden asistir los profesores de det asignatura
    res3 = '' #restricción cantidad de bloques por semana

    combinaciones_bloque_dia = instancia['asignaturas'][1]['salas'][1]['horarios']
    # print(combinaciones_bloque_dia)
    for key in instancia['asignaturas']:
    
        priority = instancia['asignaturas'][key]['prioridad'] # Rescata la prioridad de la asignatura
        bloques_semanales = instancia['asignaturas'][key]['cantidad_bloques'] # Rescata la cantidad de bloques semanales x asignatura

        # Recorrer todos los bloques y días posibles
        bloques_y_dias = {}

        for key_sala in instancia['asignaturas'][key]['salas']:
            sala_actual = key_sala
            asignatura_actual = key

            #y{asignatura}.{sala1}.{bloque}.{dia} + y{asignatura}.{sala2}.{bloque}.{dia} + ... <= 1
            
            for horario in instancia['asignaturas'][key]['salas'][key_sala]['horarios']:
                bloque = horario[0]
                dia = horario[1]
                
                y_particular = f'y{asignatura_actual}.{sala_actual}.{bloque}.{dia}' # y(asignatura).(sala).(bloque).(dia) [todas las comb posibles]
                funcion_objetivo += f' { priority } {y_particular} +'

                # Verifica si el profesor tiene el bloque disponible sin importar la sala, si no está disponible, restringe esa combi
                if tuple(horario) in instancia['asignaturas'][key]['bloques_no_disponibles']:
                    res2+= f'{y_particular} = 0;\n'
                else:
                    # Ya que los limites se deben definir solo 1 vez
                    bn += f'{y_particular},' # Esta cadena es para definirlas todas como variables binarias luego
                
                # Agrupar las variables por combinación de (bloque, día) para la restricción de `res1`
                if (bloque, dia) not in bloques_y_dias:
                    bloques_y_dias[(bloque, dia)] = []
                bloques_y_dias[(bloque, dia)].append(y_particular)


        # Generar restricciones para asegurar que solo una sala se use por asignatura, bloque y día
        for (bloque, dia), variables in bloques_y_dias.items():
            restriccion = ' + '.join(variables) + ' <= 1;\n'
            res1 += restriccion

    # Esto solamente lo hago para evitar el problema de que me quede el signo más al final, no se me ocurrio una idea más pulcra
    funcion_objetivo = funcion_objetivo[:-1]
    funcion_objetivo += ';'
    # Usamos el comando bin para denotar que son variables binarias
    bn = bn[:-1]
    bn += ';'

    archivo.write( funcion_objetivo+'\n\n')
    archivo.write( res1 )
    archivo.write( res2 )
    archivo.write( bn )

    print(f'Archivo {nombre_archivo}.lp creado.')

    # Cierra el archivo para asegurarte de que se guarde correctamente
    archivo.close()
