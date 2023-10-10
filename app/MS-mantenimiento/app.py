from flask import Flask, render_template

app = Flask(__name__)

# Datos de prueba de buses disponibles y en mantenimiento (formato JSON)
buses_disponibles = [
    {"nombre": "Bus 1", "estado": "Disponible"},
    {"nombre": "Bus 2", "estado": "Disponible"},
]

buses_mantenimiento = [
    {"nombre": "Bus 3", "estado": "Mantenimiento"},
    {"nombre": "Bus 4", "estado": "Mantenimiento"},
]

@app.route('/')
def despacho():
    return render_template('mantenimiento.html', buses_disponibles=buses_disponibles, buses_mantenimiento=buses_mantenimiento)

if __name__ == '__main__':
    app.run(debug=True)
