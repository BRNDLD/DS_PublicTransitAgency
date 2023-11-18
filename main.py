import os, json, uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logic.usuario import User

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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

@app.get("/usuario/rutas")
async def rutas(request: Request):
    tipos_de_vehiculos = set(item["tipo"] for item in programacion)
    return templates.TemplateResponse("rutas.html", {"request": request, "programacion": programacion, "tipos_de_vehiculos": tipos_de_vehiculos})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)