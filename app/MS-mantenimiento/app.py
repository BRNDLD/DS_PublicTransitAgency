from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Leer datos de vehículos desde un archivo JSON
with open('data/buses.json', 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)

# Ruta para cargar la página HTML
@app.route('/')
def mostrar_tablas():
    return render_template('mantenimiento.html', datos=vehiculos)

# En la ruta para cambiar el estado de un vehículo
@app.route('/cambiar_estado/<placa>', methods=['POST'])
def cambiar_estado(placa):
    nuevo_estado = request.json['nuevo_estado']

    for vehiculo in vehiculos:
        if vehiculo['placa'] == placa:
            vehiculo['estado'] = nuevo_estado

    with open('buses.json', 'w') as vehiculos_file:
        json.dump(vehiculos, vehiculos_file, indent=4)

    return jsonify({'nuevo_estado': nuevo_estado})

if __name__ == '__main__':
    app.run()
