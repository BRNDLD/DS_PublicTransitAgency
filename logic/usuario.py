from logic.db import DbController

class User:
    def __init__(self, db_controller: DbController):
        self.db_controller = db_controller
        self.users, self.admin, self.historial = self.db_controller.load_data()

    def validate_username(self, username: str) -> str:
        if len(username) < 6:
            return "El nombre de usuario debe tener al menos 6 caracteres."
        return None

    def validate_password(self, password: str) -> str:
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not any(char.isdigit() for char in password):
            return "La contraseña debe contener al menos un número."
        return None

    def signup(self, username: str, password: str, confirm_password: str) -> str:
        username_error = self.validate_username(username)
        password_error = self.validate_password(password)

        if username_error:
            return username_error
        if password_error:
            return password_error

        if self.db_controller.username_exists(username):
            return "El nombre de usuario ya está en uso. Por favor, elige otro."
        
        if password == confirm_password:
            success = self.db_controller.register_user(username, password)
            if success:
                return "Registro exitoso. Ahora puedes iniciar sesión."
            else:
                return "Error al registrar el usuario. Por favor, intente nuevamente."
        else:
            return "Las contraseñas no coinciden."

    def add_to_historial(self, username: str, viaje: dict) -> str:
        user_exists = self.db_controller.users_collection.find_one({'username': username})
        if not user_exists:
            return "El usuario no existe."

        self.db_controller.add_to_historial(username, viaje)
        