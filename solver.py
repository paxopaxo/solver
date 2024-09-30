
#Recibe como parametro una única instancia
def crea_modelo(instancia, nombre_archivo):
    # Crea archivo
    archivo = open(nombre_archivo+'.lp', 'w')
    # Escribe el contenido en el archivo
    funcion_objetivo = 'max: '
    bn = 'bin '
    
    for key in instancia['asignaturas']:

        priority = instancia['asignaturas'][key]['prioridad']
        funcion_objetivo += f' { priority } y{key} +'
        bn += f'y{key},'
        # print(key)

    # Esto solamente lo hago para evitar el problema de que me quede el signo más al final, no se me ocurrio una idea más pulcra
    funcion_objetivo = funcion_objetivo[:-1]
    funcion_objetivo += ';'
    # Usamos el comando bin para denotar que son variables binarias
    bn = bn[:-1]
    bn += ';'

    archivo.write( funcion_objetivo+'\n\n')
    archivo.write( bn )

    # Cierra el archivo para asegurarte de que se guarde correctamente
    archivo.close()
