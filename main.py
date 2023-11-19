import os
import json
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logic.usuario import User
from logic.MSpasajeros import PasajeroController

app = FastAPI()
templates = Jinja2Templates(directory="templates")

pasajero_controller = PasajeroController("data/users.json", "data/historial.json", "data/precios.json")

with open("data/programacion.json", "r") as json_file:
    programacion = json.load(json_file)

app.mount("/static", StaticFiles(directory="static"), name="static")

user_manager = User()


def load_data(self):
    """
    Load user, historial and precios data from JSON files.

    :returns: Tuple containing user, historial and precios data
    :rtype: Tuple[dict, dict, dict]
    """
    with open(self.users_file, 'r') as users_file:
        users_data = json.load(users_file)
    with open(self.historial_file, 'r') as historial_file:
        historial_data = json.load(historial_file)
    with open(self.precios_file, 'r') as precios_file:
        precios_data = json.load(precios_file)
    return users_data, historial_data, precios_data


@app.get("/")
async def home(request: Request):
    """
    Home page endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the home page
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
async def login(request: Request):
    """
    Login page endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the login page
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), code: str = Form(None)):
    """
    Login post endpoint.

    :param request: FastAPI request object
    :type request: Request
    :param username: User's username
    :type username: str
    :param password: User's password
    :type password: str
    :param code: Authentication code
    :type code: str
    :return: TemplateResponse based on login success or failure
    :rtype: TemplateResponse
    """
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
    """
    Signup page endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the signup page
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": None})


@app.post("/signup")
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), code: str = Form(None)):
    """
    Signup post endpoint.

    :param request: FastAPI request object
    :type request: Request
    :param username: User's username
    :type username: str
    :param password: User's password
    :type password: str
    :param confirm_password: Confirmation of user's password
    :type confirm_password: str
    :param code: Authentication code
    :type code: str
    :return: TemplateResponse based on signup success or failure
    :rtype: TemplateResponse
    """
    error = user_manager.signup(username, password, confirm_password, code)
    if error:
        return templates.TemplateResponse("signup.html", {"request": request, "error": error, "success": None})
    return templates.TemplateResponse("signup.html", {"request": request, "error": None, "success": "Registro exitoso. Ahora puedes iniciar sesión."})


@app.get("/usuario")
async def usuario(request: Request):
    """
    User panel endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the user panel
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("panelUsuario.html", {"request": request, "user_name": "Usuario"})


@app.get("/admin")
async def admin(request: Request):
    """
    Admin panel endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the admin panel
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("panelAdmin.html", {"request": request, "admin_name": "Administrador"})


@app.get("/admin/pasajeros", response_model=dict)
async def pasajeros(request: Request):
    """
    Pasajeros endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the pasajeros admin panel
    :rtype: TemplateResponse
    """
    all_historial = pasajero_controller.get_all_historial()
    usernames = pasajero_controller.get_usernames()
    selected_username = request.query_params.get("username", "")
    historial = all_historial.get(selected_username, [])
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": usernames, "selected_username": selected_username, "historial": all_historial})


@app.get("/admin/pasajeros/{username}", response_model=dict)
async def pasajero_details(request: Request, username: str):
    """
    Pasajero details endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :param username: User's username
    :type username: str
    :return: TemplateResponse for the pasajero details admin panel
    :rtype: TemplateResponse
    """
    all_historial = pasajero_controller.get_all_historial()
    return templates.TemplateResponse("pasajeros.html", {"request": request, "usernames": pasajero_controller.get_usernames(), "historial": all_historial})


@app.get("/usuario/rutas")
async def rutas(request: Request):
    """
    Rutas endpoint for the user panel.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the rutas user panel
    :rtype: TemplateResponse
    """
    tipos_de_vehiculos = set(item["tipo"] for item in programacion)
    return templates.TemplateResponse("rutas.html", {"request": request, "programacion": programacion, "tipos_de_vehiculos": tipos_de_vehiculos})


@app.get("/admin/modificarPrecios", response_model=dict)
async def modificarPrecios(request: Request):
    """
    ModificarPrecios endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the modificarPrecios admin panel
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": programacion, "pasajero_controller": pasajero_controller, "precios_data": pasajero_controller.precios_data})


@app.post("/admin/modificarPrecios")
async def modificar_precios(request: Request, precio: float = Form(...)):
    """
    ModificarPrecios post endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :param precio: New price
    :type precio: float
    :return: TemplateResponse for the modificarPrecios admin panel
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("modificarPrecios.html", {"request": request, "programacion": programacion, "pasajero_controller": pasajero_controller, "precios_data": pasajero_controller.precios_data})


@app.post("/admin/modificarPrecios/{programacion_id}")
async def guardar_precio(request: Request, programacion_id: int, precio: float = Form(...)):
    """
    Guardar precio endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :param programacion_id: Programacion ID
    :type programacion_id: int
    :param precio: New price
    :type precio: float
    :return: RedirectResponse to modificarPrecios admin panel
    :rtype: RedirectResponse
    """
    global programacion
    programacion_item = next((item for item in programacion if item["id"] == programacion_id), None)
    if not programacion_item:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    pasajero_controller.set_precio_by_id(programacion_id, precio, programacion_item)
    return RedirectResponse(url="/admin/modificarPrecios")


@app.get("/admin/modificarPrecios/{programacion_id}/eliminar")
async def eliminar_precio(request: Request, programacion_id: int):
    """
    Eliminar precio endpoint for the admin panel.

    :param request: FastAPI request object
    :type request: Request
    :param programacion_id: Programacion ID
    :type programacion_id: int
    :return: RedirectResponse to modificarPrecios admin panel
    :rtype: RedirectResponse
    """
    pasajero_controller.delete_precio_by_id(programacion_id)
    return RedirectResponse(url="/admin/modificarPrecios")


@app.get("/usuario/precios", response_model=dict)
async def precios(request: Request):
    """
    Precios endpoint for the user panel.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the precios user panel
    :rtype: TemplateResponse
    """
    with open("data/precios.json", "r") as json_file:
        precios_data = json.load(json_file)

    return templates.TemplateResponse("precios.html", {"request": request, "precios_data": precios_data})


@app.get("/usuario/pagos/{precio_id}")
async def pagos(request: Request, precio_id: int):
    """
    Pagos endpoint for the user panel.

    :param request: FastAPI request object
    :type request: Request
    :param precio_id: Precio ID
    :type precio_id: int
    :return: TemplateResponse for the pagos user panel
    :rtype: TemplateResponse
    """
    precio_data = pasajero_controller.get_precio_by_id(precio_id)
    return templates.TemplateResponse("pagos.html", {"request": request, "servicio": precio_data})


@app.post("/usuario/pagos/{precio_id}/comprar")
async def comprar(request: Request, precio_id: int, username: str = Form(...), password: str = Form(...), tarjeta: str = Form(...), fecha_expiracion: str = Form(...), cvv: str = Form(...)):
    """
    Comprar post endpoint for the user panel.

    :param request: FastAPI request object
    :type request: Request
    :param precio_id: Precio ID
    :type precio_id: int
    :param username: User's username
    :type username: str
    :param password: User's password
    :type password: str
    :param tarjeta: Credit card number
    :type tarjeta: str
    :param fecha_expiracion: Credit card expiration date
    :type fecha_expiracion: str
    :param cvv: Credit card CVV
    :type cvv: str
    :return: RedirectResponse to usuario panel
    :rtype: RedirectResponse
    """
    if user_manager.authenticate(username, password):
        servicio = pasajero_controller.get_precio_by_id(precio_id)

        if username and password and tarjeta and fecha_expiracion and cvv:
            pasajero_controller.add_to_historial(username, servicio)

            return RedirectResponse(url="/usuario", status_code=303)

    return RedirectResponse(url=f"/usuario/pagos/{precio_id}", status_code=303)


@app.get("/about")
async def about(request: Request):
    """
    About page endpoint.

    :param request: FastAPI request object
    :type request: Request
    :return: TemplateResponse for the about page
    :rtype: TemplateResponse
    """
    return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    