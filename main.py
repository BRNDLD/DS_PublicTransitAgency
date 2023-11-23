import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logic.usuario import User
from logic.MSpasajeros import PasajeroController
from logic.db import DbController

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_controller = DbController()
pasajero_controller = PasajeroController(db_controller)

app.mount("/static", StaticFiles(directory="static"), name="static")

user_manager = User(db_controller)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), code: str = Form(None)):
    if code:
        if username in user_manager.admin and user_manager.admin[username]["password"] == password and user_manager.admin[username]["code"] == code:
            return templates.TemplateResponse("panelAdmin.html", {"request": request, "admin_name": username})
    else:
        if username in user_manager.users and user_manager.users[username] == password:
            return templates.TemplateResponse("panelUsuario.html", {"request": request, "user_name": username})

    error = "Credenciales incorrectas. Por favor, verifique sus datos e intente nuevamente."
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": None})

@app.post("/signup")
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), code: str = Form(None)):
    error = user_manager.signup(username, password, confirm_password, code)
    if error:
        return templates.TemplateResponse("signup.html", {"request": request, "error": error, "success": None})
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": "Registro exitoso. Ahora puedes iniciar sesión."})

@app.get("/usuario/{username}")
async def usuario(request: Request, username: str):
    return templates.TemplateResponse("panelUsuario.html", {"request": request, "user_name": username})

@app.get("/usuario/{username}/historial")
async def historial(request: Request, username: str):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return templates.TemplateResponse("historial.html", {"request": request, "historial": pasajero_controller.get_historial_by_username(username), "user_name": username})

@app.get("/usuario/{username}/precios", response_model=dict)
async def precios(request: Request, username: str):
    precios_data = db_controller.get_precios()

    return templates.TemplateResponse("precios.html", {"request": request, "precios_data": precios_data, "user_name": username})

@app.get("/usuario/{username}/pagos/{precio_id}")
async def pagos(request: Request, username: str, precio_id: int):
    precio_data = pasajero_controller.get_precio_by_id(precio_id)
    return templates.TemplateResponse("pagos.html", {"request": request, "servicio": precio_data, "user_name": username})

@app.post("/usuario/{username}/pagos/{precio_id}/comprar")
async def comprar(request: Request, username: str, precio_id: int, password: str = Form(...), tarjeta: str = Form(...), fecha_expiracion: str = Form(...), cvv: str = Form(...)):
    
    if user_manager.authenticate(username, password):
        servicio = pasajero_controller.get_precio_by_id(precio_id)

        if username and password and tarjeta and fecha_expiracion and cvv:
            pasajero_controller.add_to_historial(username, servicio)

            return RedirectResponse(url=f"/usuario/{username}", status_code=303)

    return RedirectResponse(url=f"/usuario/{username}/pagos/{precio_id}", status_code=303)

@app.get("/usuario/{username}/rutas")
async def rutas(request: Request, username: str):
    programacion = db_controller.get_programacion()
    tipos_de_vehiculos = set(item["tipo"] for item in programacion)
    return templates.TemplateResponse("rutas.html", {"request": request, "programacion": programacion, "tipos_de_vehiculos": tipos_de_vehiculos, "user_name": username})

@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("panelAdmin.html", {"request": request, "admin_name": "Administrador"})

@app.get("/admin/pasajeros", response_model=dict)
async def pasajeros(request: Request):
    all_historial = db_controller.get_all_historial()
    usernames = db_controller.get_usernames()
    selected_username = request.query_params.get("username", "")
    historial = all_historial.get(selected_username, [])
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": usernames, "selected_username": selected_username, "historial": all_historial})

@app.get("/admin/pasajeros/{username}", response_model=dict)
async def pasajero_details(request: Request, username: str):
    all_historial = db_controller.get_all_historial()
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": db_controller.get_usernames(), "historial": all_historial})

@app.get("/admin/modificarPrecios", response_model=dict)
async def modificarPrecios(request: Request):
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": db_controller.get_programacion(), "precios_data": db_controller.get_precios_data()})

@app.post("/admin/modificarPrecios")
async def modificar_precios(request: Request, precio: float = Form(...)):
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": db_controller.get_programacion(), "precios_data": db_controller.get_precios_data()})

@app.post("/admin/modificarPrecios/{programacion_id}")
async def guardar_precio(request: Request, programacion_id: int, precio: float = Form(...)):
    programacion_item = db_controller.get_programacion_item_by_id(programacion_id)
    if not programacion_item:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    db_controller.set_precio_by_id(programacion_id, precio, programacion_item)
    return RedirectResponse(url="/admin/modificarPrecios")

@app.get("/admin/modificarPrecios/{programacion_id}/eliminar")
async def eliminar_precio(request: Request, programacion_id: int):
    db_controller.delete_precio_by_id(programacion_id)
    return RedirectResponse(url="/admin/modificarPrecios")

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    