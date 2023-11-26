import certifi
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
import logging
from pymongo import MongoClient
import pymongo

mantenimiento = FastAPI()

client = MongoClient("mongodb+srv://publictransit:qwerty32@pta.bueovsa.mongodb.net/?tls=true")
db = client["Vehiculos"]
collection = db["vehiculos"]

client = pymongo.MongoClient("mongodb+srv://publictransit:qwerty32@pta.bueovsa.mongodb.net/?tls=true", tlsCAFile=certifi.where())

templates = Jinja2Templates(directory="MS-mantenimiento/templates")

mantenimiento.mount("/static", StaticFiles(directory="MS-mantenimiento/static"), name="static")


def actualizar_listas_de_vehiculos():
    """
    Update the list of active and maintenance vehicles.
    """
    vehiculos_activos = list(collection.find({"estado": "activo"}))
    vehiculos_mantenimiento = list(collection.find({"estado": "mantenimiento"}))
    return vehiculos_activos, vehiculos_mantenimiento


@mantenimiento.get("/")
async def mostrar_tablas(request: Request):
    """
    Display tables of active and maintenance vehicles.
    """
    vehiculos_activos, vehiculos_mantenimiento = actualizar_listas_de_vehiculos()
    return templates.TemplateResponse("mantenimiento.html", {"request": request, "activos": vehiculos_activos, "mantenimiento": vehiculos_mantenimiento})


@mantenimiento.post('/cambiar_estado/{placa}')
async def cambiar_estado(placa: str, nuevo_estado: str = Form(...)):
    """
    Change the state of a vehicle.
    """
    collection.update_one({"placa": placa}, {"$set": {"estado": nuevo_estado}})
    return RedirectResponse(url='/')


@mantenimiento.post('/agregar_vehiculo')
async def agregar_vehiculo(
    placa: str = Form(...),
    nuevo_estado: str = Form(..., name="nuevo_estado"),
    tipo: str = Form(...)
):
    """
    Add a new vehicle.
    """
    if collection.count_documents({"placa": placa}) > 0:
        raise HTTPException(status_code=400, detail='La placa ya existe. Introduce una placa única.')
    elif len(placa) != 3:
        raise HTTPException(status_code=400, detail='La placa debe tener exactamente 3 dígitos.')
    else:
        nuevo_vehiculo = {
            'placa': placa,
            'estado': nuevo_estado,
            'tipo': tipo
        }
        collection.insert_one(nuevo_vehiculo)

    return RedirectResponse(url='/')

