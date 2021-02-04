import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
import json
from flask import  jsonify

"""
Métodos para conectarse a la base de datos e insertar o entregar los valores de servidores, usuarios y procesos

Estos métodos son invocados desde el archivo principal app.py

"""

def insertar_servidor(json_servidores):
    """
        Método que se usa para insertar los registros del servidor entregado por el monitor
    """
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
    """
        Método que se usa para insertar los registros de los usuarios activos entregado por el monitor
    """
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
    """
        Método que se usa para insertar los procesos del servidor entregado por el monitor
    """
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

def recuperar_informacion():
    """
        Método que se usa para devolver la información de los servidores registrados en la base de datos
    """

    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_select_query= ("select servidor_id, servidor_nombre, servidor_sistema_operativo from servidores")

        mycursor.execute(sql_select_query)

        resultado = mycursor.fetchall()

        payload = []
        content = {}
        for result in resultado:
            content = {'id': result[0], 'nombre_servidor': result[1], 'sistema_operativo': result[2]}
            payload.append(content)
            content = {}

        print(payload)
        return jsonify(payload)

    except mysql.connector.Error as error:
        print("Fallo al seleccionar data de la tabla servidores {}".format(error))
    finally:
        mycursor.close()
        cnx.close()


def recuperar_informacion_detalle(id_servidor):
    """
        Método que se usa para devolver la información del servidor registrados en la base de datos pasado por parametro
    """

    payload={}

    #Recuperamos la información del servidor entregado por parametro
    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_select_query= ("select servidor_id, servidor_nombre, servidor_sistema_operativo, servidor_fecha, servidor_version from servidores where servidor_id = '" + str(id_servidor) + "'")
        mycursor.execute(sql_select_query)
        resultado = mycursor.fetchall()

        payload['servidor'] = []
        content = {}
        for result in resultado:
            content = {'id': result[0], 'nombre_servidor': result[1], 'sistema_operativo': result[2], 'servidor_version': result[4], 'servidor_fecha': result[3]}
            payload['servidor'].append(content)
            content = {}

    except mysql.connector.Error as error:
        print("Fallo al seleccionar data de la tabla servidores {}".format(error))
    finally:
        mycursor.close()
        cnx.close()

    #Recuperamos la información de los usuarios
    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_select_query= ("select usuario_nombre, usuario_terminal, usuario_pid from usuarios where servidor_id = '" + str(id_servidor) + "'")
        mycursor.execute(sql_select_query)
        resultado = mycursor.fetchall()

        payload ['usuarios'] = []
        content = {}
        for result in resultado:
            content = {'usuario_nombre': result[0], 'usuario_terminal': result[1], 'usuario_pid': result[2]}
            payload['usuarios'].append(content)
            content = {}

    except mysql.connector.Error as error:
        print("Fallo al seleccionar data de la tabla usuarios {}".format(error))
    finally:
        mycursor.close()
        cnx.close()

    #Recuperamos la información de los procesos
    try:        
        cnx = mysql.connector.connect(option_files='mydb.conf')
        mycursor = cnx.cursor()

        sql_select_query= ("select proceso_nombre, proceso_pid, proceso_username from procesos where servidor_id = '" + str(id_servidor) + "'")
        mycursor.execute(sql_select_query)
        resultado = mycursor.fetchall()

        payload['procesos'] = []
        content = {}
        for result in resultado:
            content = {'proceso_nombre': result[0], 'proceso_pid': result[1], 'proceso_username': result[2]}
            payload['procesos'].append(content)
            content = {}

    except mysql.connector.Error as error:
        print("Fallo al seleccionar data de la tabla procesos {}".format(error))
    finally:
        mycursor.close()
        cnx.close()
    
    #Retornamos la información recoletada en formato json
    print(payload)
    return jsonify(payload)