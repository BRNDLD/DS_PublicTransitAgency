import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="MS-Programacion/templates")
app.mount("/static", StaticFiles(directory="MS-Programacion/static"), name="static")

# Define la ruta completa al archivo 'programacion.json'
ruta_json = os.path.join(os.path.dirname(__file__), 'programacion.json')

# Cargar datos desde el archivo JSON al iniciar la aplicación
def load_data():
    try:
        with open(ruta_json, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

data = load_data()

class Service(BaseModel):
    tipo: str
    ruta: str
    horario: str

@app.post('/services/')
async def create_service(service: Service):
    # Aquí no es necesario validar manualmente, FastAPI maneja la validación automáticamente
    new_service = {
        'id': len(data) + 1,
        'tipo': service.tipo,
        'ruta': service.ruta,
        'horario': service.horario,
    }

    # Agregar el nuevo servicio a la lista en memoria
    data.append(new_service)

    # Actualizar el archivo JSON con la lista completa
    with open(ruta_json, 'w') as file:
        json.dump(data, file, indent=4)

    return {"message": "Servicio creado"}


@app.get('/services/', response_model=list[Service])
def get_services():
    return data

@app.get('/')
async def read_index(request: Request):
    return templates.TemplateResponse("programacion.html", {"request": request, "data": data})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
