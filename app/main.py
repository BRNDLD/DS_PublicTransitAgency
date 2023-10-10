from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
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