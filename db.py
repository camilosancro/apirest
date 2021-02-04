import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

"""
Métodos para conectarse a la base de datos e insertar los valores de servidores, usuarios y procesos

Estos métodos son invocados desde el archivo principal app.py

"""

def insertar_servidor(json_servidores):
    try:        

        #Conexión realizada a través de archivo de parámetros.
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        date = datetime.now()
        sql_insert_query= ("insert into servidores (servidor_nombre, servidor_procesador, servidor_sistema_operativo,"
                        "servidor_version, servidor_cpu_utilizacion, servidor_fecha)"
                        "values (%(nombre_servidor)s,%(procesador)s, %(sistema_operativo)s, %(version)s,"
                        " %(cpu_uso)s, '" + str(date) + "')")
        
        #Recorremos el objeto json pasado por parametro y procedemos con el insertado de los valores    
        for json_servidor in json_servidores:
            mycursor.execute(sql_insert_query, json_servidor)

        print("Registro insertado, ID", mycursor.lastrowid)

        cnx.commit()
        print("Nuevo servidor agregado")

        # Retornamos el id insertado para pasarlo a otras tablas.
        return mycursor.lastrowid

    except mysql.connector.Error as error:
        print("Fallo al insertar en la tabla servidores {}".format(error))
    finally:
        mycursor.close()
        cnx.close()

def insertar_usuarios(json_usuarios, id_servidor):
    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_insert_query= ("insert into usuarios (servidor_id, usuario_nombre, usuario_terminal, usuario_pid)"                        
                        "values ('" + str(id_servidor) + "',%(nombre_usuario)s, %(terminal)s, %(pid_usuario)s )")
                     
        for json_usuario in json_usuarios:
            mycursor.execute(sql_insert_query, json_usuario)
            

        cnx.commit()
        print("Usuarios registrado")

    except mysql.connector.Error as error:
        print(mycursor._executed)
        print("Fallo al insertar en la tabla usuarios {}".format(error))
    finally:
        mycursor.close()
        cnx.close()

def insertar_procesos(json_procesos, id_servidor):
    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_insert_query= ("insert into procesos (servidor_id, proceso_nombre, proceso_pid, proceso_username)"                        
                        "values ('" + str(id_servidor) + "',%(nombre_proceso)s, %(pid_proceso)s, %(username)s )")
                     
        for json_proceso in json_procesos:
            mycursor.execute(sql_insert_query, json_proceso)
            

        cnx.commit()
        print("Procesos registrados")

    except mysql.connector.Error as error:
        print(mycursor._executed)
        print("Fallo al insertar en la tabla procesos {}".format(error))
    finally:
        mycursor.close()
        cnx.close()
