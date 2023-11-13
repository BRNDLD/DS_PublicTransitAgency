import os
import json
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="MS-Programacion/templates")
app.mount("/static", StaticFiles(directory="MS-Programacion/static"), name="static")

programacion_json = os.path.join(os.path.dirname(__file__), 'programacion.json')
buses_json = os.path.join(os.path.dirname(__file__), 'buses.json')
rutas_json = os.path.join(os.path.dirname(__file__), 'rutas.json')

# Cargar datos desde el archivo al iniciar la aplicación
def load_data():
    try:
        with open(programacion_json, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def load_active_buses():
    try:
        with open(buses_json, 'r') as file:
            vehicles = json.load(file)
            active_vehicles = [{"placa": vehicle["placa"], "tipo": vehicle["tipo"]} for vehicle in vehicles if vehicle["estado"] == "activo"]
            return active_vehicles
    except FileNotFoundError:
        return []

data = load_data()
active_vehicles = load_active_buses()

# Cargar rutas desde el archivo al iniciar la aplicación
def load_rutas():
    try:
        with open(rutas_json, 'r') as file:
            rutas = json.load(file)
    except FileNotFoundError:
        rutas = []
    return rutas

def save_rutas():
    with open(rutas_json, 'w') as file:
        json.dump(rutas, file, indent=4)

rutas = load_rutas()

class Service(BaseModel):
    tipo: str
    vehiculo: str
    horario: str
    ruta: Optional[str] = None

@app.post('/services/')
async def create_service(service: Service):
    try:
        new_service = {
            'id': len(data) + 1,
            'tipo': service.vehiculo.split(' - ')[0],
            'placa_vehiculo': service.vehiculo.split(' - ')[1],
            'horario': service.horario,
            'ruta': service.ruta,
            'vehiculo': service.vehiculo,
        }
        data.append(new_service)

        # Guardar los cambios en el archivo JSON de programación
        with open(programacion_json, 'w') as file:
            json.dump(data, file, indent=4)

        # Agregar la nueva ruta a la lista de rutas si no existe
        if service.ruta and service.ruta not in rutas:
            rutas.append(service.ruta)
            save_rutas()

        return new_service
    except Exception as e:
        print(f"Error creating service: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get('/services/', response_model=list[Service])
async def get_services():
    return data

# Ruta para obtener la lista de rutas
@app.get('/routes/', response_model=list[str])
def get_routes():
    return rutas

# Ruta para agregar una nueva ruta
@app.post('/routes/')
async def add_route(new_route: dict):
    try:
        route = new_route.get("route")
        if route and route not in rutas:
            rutas.append(route)
            save_rutas()
        return rutas
    except Exception as e:
        print(f"Error adding route: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete('/services/{service_id}/')
async def delete_service(service_id: int):
    try:
        service_to_delete = next((service for service in data if service["id"] == service_id), None)
        if service_to_delete:
            data.remove(service_to_delete)

            # Guardar los cambios en el archivo JSON de programación
            with open(programacion_json, 'w') as file:
                json.dump(data, file, indent=4)

            return service_to_delete
        else:
            raise HTTPException(status_code=422, detail="El servicio no existe.")
    except Exception as e:
        print(f"Error deleting service: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Ruta para eliminar una ruta
@app.delete('/routes/')
async def delete_route(route: dict):
    try:
        route_to_delete = route.get("route")
        if route_to_delete and route_to_delete in rutas:
            rutas.remove(route_to_delete)
            save_rutas()
            return rutas
        else:
            raise HTTPException(status_code=422, detail="La ruta no existe.")
    except Exception as e:
        print(f"Error deleting route: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Ruta para obtener la lista de servicios
@app.get('/services/', response_model=list[Service])
async def get_services():
    return data

@app.get('/programacion-json/', response_class=FileResponse)
async def get_programacion_json():
    return programacion_json

# Ruta para la página principal
@app.get('/', response_class=HTMLResponse)
async def read_index(request: Request):
    data = load_data()  # Cargar los datos desde el archivo JSON
    return templates.TemplateResponse("programacion.html", {"request": request, "data": data, "active_vehicles": active_vehicles, "routes": rutas})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
