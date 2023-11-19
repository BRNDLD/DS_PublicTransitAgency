import os, json, uvicorn
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from logic.usuario import User
from logic.MSpasajeros import PasajeroController

app = FastAPI()
templates = Jinja2Templates(directory="templates")

pasajero_controller = PasajeroController("data/users.json", "data/historial.json", "data/precios.json")

# Leer el archivo programacion.json
with open("data/programacion.json", "r") as json_file:
    programacion = json.load(json_file)

# Montar la configuración para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Crear una instancia de la clase User para gestionar la autenticación
user_manager = User()

# Ruta principal
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Ruta de inicio de sesión
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), code: str = Form(None)):
    if code:
        # Intento de inicio de sesión como administrador
        if username in user_manager.admin and user_manager.admin[username]["password"] == password and user_manager.admin[username]["code"] == code:
            return templates.TemplateResponse("panelAdmin.html", {"request": request, "admin_name": username})
    else:
        # Intento de inicio de sesión como usuario normal
        if username in user_manager.users and user_manager.users[username] == password:
            return templates.TemplateResponse("panelUsuario.html", {"request": request, "user_name": username})

    error = "Credenciales incorrectas. Por favor, verifique sus datos e intente nuevamente."
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

# Ruta de Registro
@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": None})

@app.post("/signup")
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), code: str = Form(None)):
    error = user_manager.signup(username, password, confirm_password, code)
    if error:
        return templates.TemplateResponse("signup.html", {"request": request, "error": error, "success": None})
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": "Registro exitoso. Ahora puedes iniciar sesión."})

@app.get("/usuario")
async def usuario(request: Request):
    return templates.TemplateResponse("panelUsuario.html", {"request": request, "user_name": "Usuario"})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("panelAdmin.html", {"request": request, "admin_name": "Administrador"})

# Nueva ruta para la lista de pasajeros y detalles del historial
@app.get("/admin/pasajeros", response_model=dict)
async def pasajeros(request: Request):
    all_historial = pasajero_controller.get_all_historial()
    usernames = pasajero_controller.get_usernames()
    selected_username = request.query_params.get("username", "")
    historial = all_historial.get(selected_username, [])
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": usernames, "selected_username": selected_username, "historial": all_historial})

@app.get("/admin/pasajeros/{username}", response_model=dict)
async def pasajero_details(request: Request, username: str):
    all_historial = pasajero_controller.get_all_historial()
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": pasajero_controller.get_usernames(), "historial": all_historial})

@app.get("/usuario/rutas")
async def rutas(request: Request):
    tipos_de_vehiculos = set(item["tipo"] for item in programacion)
    return templates.TemplateResponse("rutas.html", {"request": request, "programacion": programacion, "tipos_de_vehiculos": tipos_de_vehiculos})

# Nueva ruta para la modificación de precios
@app.get("/admin/modificarPrecios", response_model=dict)
async def modificarPrecios(request: Request):
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": programacion, "pasajero_controller": pasajero_controller, "precios_data": pasajero_controller.precios_data})

@app.post("/admin/modificarPrecios")
async def modificar_precios(request: Request, precio: float = Form(...)):
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": programacion, "pasajero_controller": pasajero_controller, "precios_data": pasajero_controller.precios_data})

@app.post("/admin/modificarPrecios/{programacion_id}")
async def guardar_precio(request: Request, programacion_id: int, precio: float = Form(...)):
    global programacion
    programacion_item = next((item for item in programacion if item["id"] == programacion_id), None)
    if not programacion_item:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    pasajero_controller.set_precio_by_id(programacion_id, precio, programacion_item)
    return RedirectResponse(url="/admin/modificarPrecios")

@app.get("/admin/modificarPrecios/{programacion_id}/eliminar")
async def eliminar_precio(request: Request, programacion_id: int):
    pasajero_controller.delete_precio_by_id(programacion_id)
    return RedirectResponse(url="/admin/modificarPrecios")

# Nueva ruta para la lista de precios
@app.get("/usuario/precios", response_model=dict)
async def precios(request: Request):
    # Leer el archivo precios.json
    with open("data/precios.json", "r") as json_file:
        precios_data = json.load(json_file)

    return templates.TemplateResponse("precios.html", {"request": request, "precios_data": precios_data})

# Nueva ruta para la compra de tickets
@app.get("/usuario/pagos/{precio_id}")
async def usuario_pagos(request: Request, precio_id: int):
    # Aquí puedes implementar la lógica de compra de tickets
    # (por ejemplo, mostrar un formulario de pago, procesar la transacción, etc.)
    return templates.TemplateResponse("precios.html", {"request": request, "precio_id": precio_id})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)