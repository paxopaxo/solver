#Recibe como parametro una única instancia
def crea_modelo(instancia, nombre_archivo):
    # Crea archivo
    archivo = open(nombre_archivo+'.lp', 'w')
    # Escribe el contenido en el archivo
    funcion_objetivo = 'max: '
    bn = 'bin '
    res1 = '' #restricción la clase no puede ocurrir en distintas en distintas salas a la misma hora y dia.
    res2 = '' #restricción horarios que no pueden asistir los profesores de det asignatura
    res3 = '' #restricción cantidad de bloques por semana
    res4 = '' #restriccion no pueden haber dos salas en un mismo horario asignadas a distintas clases. solo se puede usar la sala1 vez
    res5 = '' #reestricción losbloques deben ser consecutivos
    res_aux = ''  # Restricción de uso de bloques consecutivos
    res6 = ''

    # Agrupación de todas las combinaciones (bloque, día) para todas las asignaturas
    bloques_y_dias_global = {}

    for key in instancia['asignaturas']:
    
        priority = instancia['asignaturas'][key]['prioridad'] # Rescata la prioridad de la asignatura
        bloques_semanales = instancia['asignaturas'][key]['cantidad_bloques'] # Rescata la cantidad de bloques semanales x asignatura

        # Recorrer todos los bloques y días posibles
        bloques_y_dias = {}

        # Lista para almacenar todas las variables de decisión de una asignatura para res3
        variables_asignatura_semana = []
        variables_auxiliares = []
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
                # elif bloque == 7 and bloques_semanales == 2:
                    # res2+= f'y{asignatura_actual}.{sala_actual}.{bloque}.{dia}=0;\n'
                else:
                    # Ya que los limites se deben definir solo 1 vez
                    bn += f'{y_particular},' # Esta cadena es para definirlas todas como variables binarias luego

                # Para asignaturas donde hayan dos bloques:
                if bloques_semanales == 2 and bloque <7 :
                    aux_variable = f'auxy{asignatura_actual}.{sala_actual}.{bloque}.{dia}'
                    variables_auxiliares.append(aux_variable)
                    bn += f'{aux_variable},'  # Definir la variable auxiliar como binaria
                    # Restricción de bloques consecutivos utilizando variable auxiliar
                    res5 += f'y{asignatura_actual}.{sala_actual}.{bloque}.{dia} + y{asignatura_actual}.{sala_actual}.{bloque + 1}.{dia} -1 <=  {aux_variable};\n'
                    # res6 += f'{aux_variable} <= y{asignatura_actual}.{sala_actual}.{bloque}.{dia};\n'
                    if bloque <= 5:
                        res6 += f' y{asignatura_actual}.{sala_actual}.{bloque}.{dia} + y{asignatura_actual}.{sala_actual}.{bloque+1}.{dia} + y{asignatura_actual}.{sala_actual}.{bloque+2}.{dia}<= 2 ;\n'
                    # if bloque == 6:
                    #     res6 += f' y{asignatura_actual}.{sala_actual}.{bloque}.{dia} + y{asignatura_actual}.{sala_actual}.{bloque+1}.{dia}<= 2 ;\n'
                    # res6 += f'{aux_variable} <= y{asignatura_actual}.{sala_actual}.{bloque+1}.{dia};\n'
                    res6 += f'y{asignatura_actual}.{sala_actual}.{bloque}.{dia} <= y{asignatura_actual}.{sala_actual}.{bloque+1}.{dia};\n'

                # Agrupar las variables por combinación de (bloque, día) para la restricción de `res1`
                if (bloque, dia) not in bloques_y_dias:
                    bloques_y_dias[(bloque, dia)] = []
                bloques_y_dias[(bloque, dia)].append(y_particular)

                # Agrupar para restricción global (res4)
                if (bloque, dia) not in bloques_y_dias_global:
                    bloques_y_dias_global[(bloque, dia)] = []
                bloques_y_dias_global[(bloque, dia)].append(y_particular)
                
                # Agregar la variable de decisión a la lista para res3
                variables_asignatura_semana.append(y_particular)

        # Agregar la restricción para la suma de variables auxiliares
        if variables_auxiliares:
            res51 = ' + '.join(variables_auxiliares) + f' <= 1;\n'
            # print('res5')
            # print(res51)
            res_aux += res51

        # Generar restricciones para asegurar que solo una sala se use por asignatura, bloque y día
        for (bloque, dia), variables in bloques_y_dias.items():
            restriccion = ' + '.join(variables) + ' <= 1;\n'
            res1 += restriccion
        
        # # Generar restricción para que la asignatura solo tenga `bloques_semanales` asignados en la semana
        # restriccion_semana = ' + '.join(variables_asignatura_semana) + f' <= {bloques_semanales};\n'
        # res3 += restriccion_semana

        # Generar restricción para que la asignatura solo tenga `bloques_semanales` asignados en la semana
        # Si la prioridad es mayor a 5 debe elegirse si o si.
        if priority > 5:
            restriccion_semana = ' + '.join(variables_asignatura_semana) + f' = {bloques_semanales};\n'
        else:
            restriccion_semana = ' + '.join(variables_asignatura_semana) + f' <= {bloques_semanales};\n'
        res3 += restriccion_semana

    
    # Generar la restricción para que no haya más de una sala usándose simultáneamente en el mismo bloque y día
    for (bloque, dia), variables in bloques_y_dias_global.items():
        restriccion = ' + '.join(variables) + ' <= 1;\n'
        res4 += restriccion

    # Esto solamente lo hago para evitar el problema de que me quede el signo más al final, no se me ocurrio una idea más pulcra
    funcion_objetivo = funcion_objetivo[:-1]
    funcion_objetivo += ';'
    # Usamos el comando bin para denotar que son variables binarias
    bn = bn[:-1]
    bn += ';'

    archivo.write( funcion_objetivo+'\n\n')
    archivo.write( res1 )
    archivo.write( res2 )
    archivo.write( res3 )
    archivo.write( res4 )
    archivo.write( res5 )
    archivo.write( res6 )
    archivo.write( res_aux )
    archivo.write( bn )

    print(f'Archivo {nombre_archivo}.lp creado.')

    # Cierra el archivo para asegurarte de que se guarde correctamente
    archivo.close()
