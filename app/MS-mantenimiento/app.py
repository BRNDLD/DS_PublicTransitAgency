import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def mantenimiento():
    return render_template('mantenimiento.html')


if __name__ == '__main__':
    app.run(debug=True)
