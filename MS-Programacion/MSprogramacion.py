import os
import json
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="MS-Programacion/templates")
app.mount("/static", StaticFiles(directory="MS-Programacion/static"), name="static")

ruta_json = os.path.join(os.path.dirname(__file__), 'programacion.json')
ruta_buses_json = os.path.join(os.path.dirname(__file__), 'buses.json')

def load_data():
    try:
        with open(ruta_json, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

data = load_data()

def load_active_buses():
    try:
        with open(ruta_buses_json, 'r') as file:
            vehicles = json.load(file)
            active_vehicles = [{"placa": vehicle["placa"], "tipo": vehicle["tipo"]} for vehicle in vehicles if vehicle["estado"] == "activo"]
            return active_vehicles
    except FileNotFoundError:
        return []

active_vehicles = load_active_buses()

class Service(BaseModel):
    vehiculo: str 
    horario: str

@app.post('/services/')
async def create_service(service: Service):
    new_service = {
        'id': len(data) + 1,
        'tipo': service.vehiculo.split(' - ')[0],  
        'placa_vehiculo': service.vehiculo.split(' - ')[1],  
        'horario': service.horario,
        'vehiculo': service.vehiculo, 
    }
    data.append(new_service)
    with open(ruta_json, 'w') as file:
        json.dump(data, file, indent=4)
    return new_service

@app.get('/services/', response_model=list[Service])
def get_services():
    return data

@app.get('/')
async def read_index(request: Request):
    return templates.TemplateResponse("programacion.html", {"request": request, "data": data, "active_vehicles": active_vehicles})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
