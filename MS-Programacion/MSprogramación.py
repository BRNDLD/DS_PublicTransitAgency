import os
from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Define la ruta completa al archivo 'programacion.json'
ruta_json = os.path.join(os.path.dirname(__file__), 'programacion.json')

# Cargar datos desde el archivo JSON
def load_data():
    with open(ruta_json, 'r') as file:
        data = json.load(file)
    return data

data = load_data()  # Cargar datos al iniciar la aplicación

@app.route('/')
def index():
    return render_template('programacion.html', data=data)

@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'GET':
        return jsonify(data)

    if request.method == 'POST':
        new_service = {
            'id': len(data) + 1,
            'tipo': request.json['tipo'],
            'ruta': request.json['ruta'],
            'horario': request.json['horario'],
        }
        data.append(new_service)
        
        # Actualizar el archivo JSON con el nuevo servicio
        with open(ruta_json, 'w') as file:
            json.dump(data, file, indent=4)

        return jsonify({'message': 'Servicio creado', 'service': new_service}), 201

if __name__ == '__main__':
    app.run(debug=True)
