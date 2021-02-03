#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from datetime import datetime
import json
import csv


app = Flask(__name__)

#Servicio de registro de información enviada por el monitor

@app.route('/registrar', methods=['POST'])
def registrar():
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

  
    return jsonify({
        "mensaje": "Información registrada correctamente.",
    })




if __name__ == '__main__':
    app.run(debug=True, port=8080)
