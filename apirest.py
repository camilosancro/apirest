from flask import Flask, jsonify, request
import json
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'


@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    servidor = data['nombre']
    usurio = data['usuarios']
    procesos = data['procesos']
    return jsonify({
        "nombre": servidor,
        "usuario 1": usurio[0],
        "Proceso 2": procesos[0]["proceso"]
    })





if __name__ == '__main__':
    app.run(debug=True, port=8080)
