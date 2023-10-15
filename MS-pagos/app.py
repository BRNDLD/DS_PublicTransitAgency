import json
from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

# Ruta para mostrar tablas
@app.route('/')
def mostrar_tablas():
    return render_template('transacciones.html', datos=obtener_transacciones())

# Ruta para realizar un pago
@app.route('/realizar_pago', methods=['POST'])
def realizar_pago():
    data = request.get_json()

    # Validar la información del pago
    if 'tarjeta' not in data or 'monto' not in data:
        return jsonify({'mensaje': 'Faltan datos obligatorios'}), 400

    tarjeta = data['tarjeta']
    monto = data['monto']

    transaccion_exitosa = simular_pasarela_de_pago(tarjeta, monto)

    if transaccion_exitosa:
        # Registra la transacción en el archivo JSON de transacciones
        registrar_transaccion(tarjeta, monto)

        return jsonify({'mensaje': 'Pago exitoso'})
    else:
        return jsonify({'mensaje': 'Pago fallido'}), 400

def simular_pasarela_de_pago(tarjeta, monto):
    return True  

def obtener_transacciones():
    transacciones = []

    # Verificar si el archivo "transacciones.json" existe
    if os.path.exists('transacciones.json'):
        # Cargar transacciones existentes desde el archivo JSON
        with open('transacciones.json', 'r') as file:
            transacciones = json.load(file)

    return transacciones

def registrar_transaccion(tarjeta, monto):
    transacciones = obtener_transacciones()

    # Agregar la nueva transacción
    nueva_transaccion = {'tarjeta': tarjeta, 'monto': monto}
    transacciones.append(nueva_transaccion)

    # Guardar las transacciones actualizadas en el archivo JSON
    with open('transacciones.json', 'w') as file:
        json.dump(transacciones, file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
