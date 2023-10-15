from flask import Flask, flash, render_template, jsonify, request, redirect
import json, os

mantenimiento = Flask(__name__)

# Obtén el directorio raíz actual (donde se ejecuta el script)
directorio_raiz = os.getcwd()

print("Directorio Raíz:", directorio_raiz)

# Configurar la clave secreta
mantenimiento.secret_key = '001'  # Reemplaza 'tu_clave_secreta_aqui' con una cadena segura

# Leer datos de vehículos desde un archivoJSON
with open('data/buses.json', 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)

# Ruta para cargar la página HTML
@mantenimiento.route('/')
def mostrar_tablas():
    return render_template('mantenimiento.html', datos=vehiculos)

# Ruta para cambiar el estado de un vehículo
@mantenimiento.route('/cambiar_estado/<placa>', methods=['POST'])
def cambiar_estado(placa):
    nuevo_estado = request.json['nuevo_estado']

    for vehiculo in vehiculos:
        if vehiculo['placa'] == placa:
            vehiculo['estado'] = nuevo_estado

    with open('data/buses.json', 'w') as vehiculos_file:
        json.dump(vehiculos, vehiculos_file, indent=4)

    return jsonify({'nuevo_estado': nuevo_estado})

# Ruta y formulario para agregar vehículos
@mantenimiento.route('/agregar_vehiculo', methods=['POST'])
def agregar_vehiculo():
    placa = request.form['placa']
    estado = request.form['estado']
    tipo = request.form['tipo']  # Obtén el valor del campo "tipo de vehículo"

    # Validar que la placa sea única
    placas_existentes = [vehiculo['placa'] for vehiculo in vehiculos]
    if placa in placas_existentes:
        flash('La placa ya existe. Introduce una placa única.', 'error')
    else:
        nuevo_vehiculo = {
            'placa': placa,
            'estado': estado,
            'tipo': tipo  # Agrega el atributo "tipo de vehículo"
        }
        vehiculos.append(nuevo_vehiculo)

        with open('data/buses.json', 'w') as vehiculos_file:
            json.dump(vehiculos, vehiculos_file, indent=4)

    return redirect('/')

if __name__ == '__main__':
    mantenimiento.run()
