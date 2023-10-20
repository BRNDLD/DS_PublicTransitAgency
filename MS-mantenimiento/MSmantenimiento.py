from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json, os, uvicorn

mantenimiento = FastAPI()

# Define la ruta completa al archivo 'buses.json'
ruta_json = os.path.join(os.path.dirname(__file__), 'buses.json')

# Leer datos de vehículos desde el archivo JSON
with open(ruta_json, 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)

# Configurar la clave secreta
mantenimiento.secret_key = '001'

# Configurar la carpeta de plantillas para Jinja2
templates = Jinja2Templates(directory="MS-mantenimiento/templates")

# Configurar la gestión de archivos estáticos para servir CSS y otros archivos estáticos
mantenimiento.mount("/static", StaticFiles(directory="MS-mantenimiento/static"), name="static")

def actualizar_listas_de_vehiculos():
    # Lista separada para vehículos en estado "activo"
    vehiculos_activos = [vehiculo for vehiculo in vehiculos if vehiculo['estado'] == 'activo']
    
    # Lista separada para vehículos en estado "mantenimiento"
    vehiculos_mantenimiento = [vehiculo for vehiculo in vehiculos if vehiculo['estado'] == 'mantenimiento']
    
    return vehiculos_activos, vehiculos_mantenimiento

@mantenimiento.get("/")
async def mostrar_tablas(request: Request):
    vehiculos_activos, vehiculos_mantenimiento = actualizar_listas_de_vehiculos()
    return templates.TemplateResponse("mantenimiento.html", {"request": request, "activos": vehiculos_activos, "mantenimiento": vehiculos_mantenimiento})

# Ruta para cambiar el estado de un vehículo
@mantenimiento.post('/cambiar_estado/{placa}')
async def cambiar_estado(placa: str, nuevo_estado: str = Form(...)):
    for vehiculo in vehiculos:
        if vehiculo['placa'] == placa:
            # Actualiza el estado del vehículo
            vehiculo['estado'] = nuevo_estado

            vehiculos_activos, vehiculos_mantenimiento = actualizar_listas_de_vehiculos()

    with open(ruta_json, 'w') as vehiculos_file:
        json.dump(vehiculos, vehiculos_file, indent=4)

    return RedirectResponse(url='/')

# Ruta y formulario para agregar vehículos
@mantenimiento.post('/agregar_vehiculo')
async def agregar_vehiculo(
        placa: str = Form(...),
        estado: str = Form(..., name="nuevo_estado"),
        tipo: str = Form(...)
    ):
    placas_existentes = [vehiculo['placa'] for vehiculo in vehiculos]
    if placa in placas_existentes:
        raise HTTPException(status_code=400, detail='La placa ya existe. Introduce una placa única.')
    elif len(placa) != 3:
        raise HTTPException(status_code=400, detail='La placa debe tener exactamente 3 dígitos.')
    else:
        nuevo_vehiculo = {
            'placa': placa,
            'estado': estado,
            'tipo': tipo
        }
        vehiculos.append(nuevo_vehiculo)

        vehiculos_activos, vehiculos_mantenimiento = actualizar_listas_de_vehiculos()

        with open(ruta_json, 'w') as vehiculos_file:
            json.dump(vehiculos, vehiculos_file, indent=4)

    return RedirectResponse(url='/')

if __name__ == '__main__':
    uvicorn.run(mantenimiento, host="127.0.0.1", port=8000)
