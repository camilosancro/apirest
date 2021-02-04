#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Este script expone servicios para registrar o consultar la información de servidores enviada por los monitores

"""

#Importamos los módulos requeridos
from flask import Flask, jsonify, request
from datetime import datetime
import json
import csv
import db


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Expones el servicio registrar para el método post

@app.route('/registrar', methods=['POST'])
def registrar():

    #recolectamos la información enviada por la aplicación de monitoreo
    data = request.get_json()
    ip = data['ip']
    servidor = data['servidor']
    usuarios = data['usuarios']
    procesos = data['procesos']

    #Convertir JSON  a CSV

    date = datetime.now()
    nombrearchivo = ip + '_' + str(date) + '.csv'
    print(nombrearchivo)
 
    data_file = open( nombrearchivo, 'w') 
    cabeceras = ['nombre_servidor', 'procesador', 'sistema_operativo', 'version', 'cpu_uso', 'nombre_usuario', 'terminal', 'pid_usuario', 'nombre_proceso', 'pid_proceso', 'username']

    writer = csv.DictWriter(data_file, fieldnames=cabeceras)
    writer.writeheader()
    
    for dato in servidor:
        writer.writerow(dato)

    for usuario in usuarios:
        writer.writerow(usuario)

    for proceso in procesos:
        writer.writerow(proceso)
        
    data_file.close()

    # Fin Convertir CSV

    # Convertir Json a Texto

    nombrearchivo = ip + '_' + str(date) + '.txt'
    data_file = open( nombrearchivo, 'w') 
    json_string = json.dumps(data)
    data_file.write(json_string)
    data_file.close()

    #  Fin Json a Texto

    # insertar registros en la base de datos

    id_insertado = db.insertar_servidor(servidor)

    db.insertar_usuarios(usuarios, id_insertado)
    
    db.insertar_procesos(procesos, id_insertado)

    # fin registros en la base de datos 

    #En caso de éxito, retornamos un mensaje de éxito
    return jsonify({
        "mensaje": "Información registrada correctamente.",
    })

# Servicios de consulta para todos los servidores registrados o por uno en particular

@app.route('/servidores', methods=['GET'])
def resultado_servidores():
    resultado = db.recuperar_informacion()
    return resultado

@app.route('/servidores/<string:id_servidor>', methods=['GET'])
def resultado_servidore(id_servidor):
    resultado = db.recuperar_informacion_detalle(id_servidor)
    return resultado


if __name__ == '__main__':
    app.run(debug=True, port=8080)
