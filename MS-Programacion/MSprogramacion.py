from typing import Optional
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from typing import List
from fastapi import Path
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="MS-Programacion/templates")

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["Vehiculos"]
collection_programacion = db["Programacion"]
collection_rutas = db["Rutas"]
collection_vehiculos = db["vehiculos"]


class Service(BaseModel):
    """
    Service model.
    """
    tipo: str
    vehiculo: str
    horario: str
    ruta: Optional[str] = None


@app.post('/services/')
async def create_service(service: Service):
    """
    Route for creating a service.
    """
    try:
        tipo, placa_vehiculo = service.vehiculo.split(' - ')
        new_service = {
            'tipo': tipo,
            'placa_vehiculo': placa_vehiculo,
            'horario': service.horario,
            'ruta': service.ruta,
            'vehiculo': service.vehiculo,
        }
        result = collection_programacion.insert_one(new_service)

        new_service['_id'] = str(result.inserted_id)

        return new_service
    except Exception as e:
        print(f"Error creating service: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get('/services/', response_model=List[Service])
async def get_services():
    """
    Route for getting all services.
    """
    return list(collection_programacion.find())


@app.get('/routes/', response_model=List[str])
async def get_routes():
    """
    Route for getting all routes.
    """
    try:
        routes = list(collection_rutas.find({}, {"_id": 0, "item": 1}))
        routes_list = [route["item"] for route in routes if "item" in route]
        return routes_list
    except Exception as e:
        print(f"Error getting routes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post('/routes/')
async def add_route(new_route: dict):
    """
    Route for adding a new route.
    """
    try:
        route = new_route.get("route")
        if route and route not in collection_rutas.distinct("item"):
            collection_rutas.insert_one({"item": route})
        return list(collection_rutas.distinct("item"))
    except Exception as e:
        print(f"Error adding route: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete('/services/{service_id}/')
async def delete_service(service_id: str = Path(..., description="ID del servicio")):
    """
    Route for deleting a service.
    """
    try:
        if service_id:
            result = collection_programacion.delete_one({"_id": service_id})
            if result.deleted_count == 0:
                raise HTTPException(status_code=422, detail="El servicio no existe.")
            return result.raw_result
        else:
            raise HTTPException(status_code=400, detail="service_id no debe ser None o undefined")
    except Exception as e:
        print(f"Error deleting service: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete('/routes/')
async def delete_route(route: dict):
    """
    Route for deleting a route.
    """
    try:
        route_to_delete = route.get("route")
        result = collection_rutas.delete_one({"item": route_to_delete})
        if result.deleted_count == 0:
            raise HTTPException(status_code=422, detail="La ruta no existe.")
        return list(collection_rutas.distinct("item"))
    except Exception as e:
        print(f"Error deleting route: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get('/', response_class=HTMLResponse)
async def read_index(request: Request):
    """
    Route for the main page.
    """
    try:
        data = list(collection_programacion.find())

        all_routes = list(collection_rutas.find({}, {"_id": 0, "item": 1}))

        routes = [route["item"] for route in all_routes if "item" in route]

        active_vehicles = list(collection_vehiculos.find({"estado": "activo"}))

        print("Routes from MongoDB:", routes)
        print("All routes from MongoDB:", all_routes)

        return templates.TemplateResponse(
            "programacion.html",
            {"request": request, "data": data, "routes": routes, "active_vehicles": active_vehicles}
        )
    except Exception as e:
        print(f"Error in read_index: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

