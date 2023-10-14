from flask import Flask, flash, render_template, jsonify, request, redirect
import json

app = Flask(__name__)

# Configurar la clave secreta
app.secret_key = '001'  # Reemplaza 'tu_clave_secreta_aqui' con una cadena segura

# Leer datos de vehículos desde un archivo JSON
with open('data/buses.json', 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)

# Ruta para cargar la página HTML
@app.route('/')
def mostrar_tablas():
    return render_template('mantenimiento.html', datos=vehiculos)

# Ruta para cambiar el estado de un vehículo
@app.route('/cambiar_estado/<placa>', methods=['POST'])
def cambiar_estado(placa):
    nuevo_estado = request.json['nuevo_estado']

    for vehiculo in vehiculos:
        if vehiculo['placa'] == placa:
            vehiculo['estado'] = nuevo_estado

    with open('data/buses.json', 'w') as vehiculos_file:
        json.dump(vehiculos, vehiculos_file, indent=4)

    return jsonify({'nuevo_estado': nuevo_estado})

# Ruta y formulario para agregar vehículos
@app.route('/agregar_vehiculo', methods=['POST'])
def agregar_vehiculo():
    placa = request.form['placa']
    estado = request.form['estado']

    # Validar que la placa sea única
    placas_existentes = [vehiculo['placa'] for vehiculo in vehiculos]
    if placa in placas_existentes:
        flash('La placa ya existe. Introduce una placa única.', 'error')
    else:
        nuevo_vehiculo = {
            'placa': placa,
            'estado': estado
        }
        vehiculos.append(nuevo_vehiculo)

        with open('data/buses.json', 'w') as vehiculos_file:
            json.dump(vehiculos, vehiculos_file, indent=4)

    return redirect('/')

if __name__ == '__main__':
    app.run()
