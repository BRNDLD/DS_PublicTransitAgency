import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia 'tu_clave_secreta' a una clave secreta segura

# Función para cargar datos de usuarios y administradores desde archivos JSON
def cargar_datos():
    users_file_path = os.path.join("app","data", "users.json")
    admin_file_path = os.path.join("app","data", "admin.json")

    with open(users_file_path, 'r') as users_file:
        users = json.load(users_file)
    with open(admin_file_path, 'r') as admin_file:
        admin = json.load(admin_file)
    return users, admin

@app.route('/')
def home():
    return render_template('home.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('code')

        users, admin = cargar_datos()

        if username in users and password == users[username]:
            session['username'] = username
            return redirect(url_for('usuario'))
        elif username in admin and password == admin[username]["password"]:
            if 'code' in admin[username] and code == admin[username]['code']:
                session['username'] = username
                return redirect(url_for('admin'))
            else:
                error_message = "Código de administrador incorrecto"
                return render_template('login.html', error=error_message)
        else:
            error_message = "Credenciales incorrectas"
            return render_template('login.html', error=error_message)

    return render_template('login.html')

# Rutas para usuario y administrador
@app.route('/usuario')
def usuario():
    if 'username' in session:
        username = session['username']  # Obtén el nombre de usuario de la sesión
        return render_template('panelUsuario.html', user_name=username)
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session:
        username = session['username']  # Obtén el nombre de usuario de la sesión
        return render_template('panelAdmin.html', admin_name=username)
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        code = request.form.get('code')

        users, admin = cargar_datos()

        if username in users or username in admin:
            error_message = "El nombre de usuario ya está en uso. Por favor, elige otro."
            return render_template('signup.html', error=error_message)

        if password == confirm_password:
            if code:
                # Registro como administrador
                admin[username] = {
                    "password": password,
                    "code": code
                }
                with open(os.path.join("data", "admin.json"), 'w') as admin_file:
                    json.dump(admin, admin_file)
            else:
                # Registro como usuario
                users[username] = password
                with open(os.path.join("data", "users.json"), 'w') as users_file:
                    json.dump(users, users_file)

            success_message = "Registro exitoso. Ahora puedes iniciar sesión."
            return render_template('signup.html', success=success_message)
        else:
            error_message = "Las contraseñas no coinciden."
            return render_template('signup.html', error=error_message)

    return render_template('signup.html')

@app.route('/horarios')
def horarios():
    return render_template('horarios.html')

@app.route('/rutas')
def rutas():
    return render_template('rutas.html')

@app.route('/precios')
def precios():
    return render_template('precios.html')

if __name__ == '__main__':
    app.run(debug=True)