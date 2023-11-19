from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
import logging
from pymongo import MongoClient

#app name
mantenimiento = FastAPI()

# Conectar a la base de datos MongoDB
client = MongoClient("mongodb+srv://Miche17:auristeamo32@cluster0.6ojhz7l.mongodb.net/")
db = client["Vehiculos"]
collection = db["vehiculos"]

# Configurar la carpeta de plantillas para Jinja2
templates = Jinja2Templates(directory="MS-mantenimiento/templates")

# Configurar la gestión de archivos estáticos para servir CSS y otros archivos estáticos
mantenimiento.mount("/static", StaticFiles(directory="MS-mantenimiento/static"), name="static")

def actualizar_listas_de_vehiculos():
    vehiculos_activos = list(collection.find({"estado": "activo"}))
    vehiculos_mantenimiento = list(collection.find({"estado": "mantenimiento"}))
    return vehiculos_activos, vehiculos_mantenimiento

@mantenimiento.get("/")
async def mostrar_tablas(request: Request):
    vehiculos_activos, vehiculos_mantenimiento = actualizar_listas_de_vehiculos()
    return templates.TemplateResponse("mantenimiento.html", {"request": request, "activos": vehiculos_activos, "mantenimiento": vehiculos_mantenimiento})

# Ruta para cambiar el estado de un vehículo
@mantenimiento.post('/cambiar_estado/{placa}')
async def cambiar_estado(placa: str, nuevo_estado: str = Form(...)):
    collection.update_one({"placa": placa}, {"$set": {"estado": nuevo_estado}})
    return RedirectResponse(url='/')

from bson import ObjectId  # Importa la clase ObjectId desde la biblioteca bson

# ...

@mantenimiento.post('/agregar_vehiculo')
async def agregar_vehiculo(
    placa: str = Form(...),
    nuevo_estado: str = Form(..., name="nuevo_estado"),
    tipo: str = Form(...)
):
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
        collection.insert_one(nuevo_vehiculo)  # No incluyas "_id" en el documento a insertar

    return RedirectResponse(url='/')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(mantenimiento, host="127.0.0.1", port=8000)
