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

    nombrearchivo = ip + '.csv'
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

    return jsonify({
        "nombre": servidor[0]['nombre_servidor'],
        "usuario 1": usuarios[0]['nombre_usuario'],
       # "Proceso 2": procesos[0]["nombre"]
    })




if __name__ == '__main__':
    app.run(debug=True, port=8080)
