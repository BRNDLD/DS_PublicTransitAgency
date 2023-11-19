import json
import os
import re


class User:
    """
    Class representing a user in the system.
    """

    def __init__(self):
        """
        Initialize a User object.

        Loads user, admin and historial data from JSON files and initializes the object.

        :returns: User object
        :rtype: User
        """
        self.users, self.admin, self.historial = self.load_data()


    def load_data(self):
        """
        Load user, admin and historial data from JSON files.

        :returns: Tuple containing user, admin and historial data
        :rtype: Tuple[dict, dict, dict]
        """
        with open(os.path.join("data", "users.json"), 'r') as users_file:
            users = json.load(users_file)
        with open(os.path.join("data", "admin.json"), 'r') as admin_file:
            admin = json.load(admin_file)
        with open(os.path.join("data", "historial.json"), 'r') as historial_file:
            historial = json.load(historial_file)
        return users, admin, historial


    def save_data(self):
        """
        Save user, admin and historial data to JSON files.
        """
        with open(os.path.join("data", "users.json"), 'w') as users_file:
            json.dump(self.users, users_file)
        with open(os.path.join("data", "admin.json"), 'w') as admin_file:
            json.dump(self.admin, admin_file)
        with open(os.path.join("data", "historial.json"), 'w') as historial_file:
            json.dump(self.historial, historial_file)


    def authenticate(self, username, password):
        """
        Authenticate a user or admin.

        :param username: The username to authenticate.
        :type username: str
        :param password: The password to authenticate.
        :type password: str
        :returns: True if the authentication is successful, False otherwise.
        :rtype: bool
        """
        return (username in self.users and self.users[username] == password) or \
               (username in self.admin and self.admin[username]['password'] == password)


    def validate_username(self, username):
        """
        Validate the username for registration.

        :param username: The username to be validated.
        :type username: str
        :returns: Error message if the validation fails, None otherwise.
        :rtype: str or None
        """
        if len(username) < 6:
            return "El nombre de usuario debe tener al menos 6 caracteres."
        return None


    def validate_password(self, password):
        """
        Validate the password for registration.

        :param password: The password to be validated.
        :type password: str
        :returns: Error message if the validation fails, None otherwise.
        :rtype: str or None
        """
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not any(char.isdigit() for char in password):
            return "La contraseña debe contener al menos un número."
        return None


    def validate_code(self, code):
        """
        Validate the code for registration.

        :param code: The code to be validated.
        :type code: str
        :returns: Error message if the validation fails, None otherwise.
        :rtype: str or None
        """
        if not re.match(r'^[0-9]{3}[a-zA-Z]{3}$', code):
            return "El código debe tener el formato 3 números y 3 letras."
        if code in self.admin:
            return "El código ya está en uso."
        return None


    def signup(self, username, password, confirm_password, code):
        """
        Register a new user or admin in the system.

        :param username: The username to register.
        :type username: str
        :param password: The password for the user.
        :type password: str
        :param confirm_password: The confirmation of the password.
        :type confirm_password: str
        :param code: The code for admin registration (optional).
        :type code: str
        :returns: Success message or an error message.
        :rtype: str
        """
        username_error = self.validate_username(username)
        password_error = self.validate_password(password)
        code_error = None

        if code:
            code_error = self.validate_code(code)

        if username_error:
            return username_error
        if password_error:
            return password_error
        if code_error:
            return code_error

        if username in self.users or username in self.admin:
            return "El nombre de usuario ya está en uso. Por favor, elige otro."
        
        if password == confirm_password:
            if code:
                self.admin[username] = {
                    "password": password,
                    "code": code
                }
            else:
                self.users[username] = password
            self.save_data()
            return "Registro exitoso. Ahora puedes iniciar sesión."
        else:
            return "Las contraseñas no coinciden."


    def add_to_historial(self, username, servicio):
        """
        Add a service to the user's history.

        :param username: The username of the user.
        :type username: str
        :param servicio: The service to add to the history.
        :type servicio: dict
        """
        if username not in self.users and username not in self.admin:
            return "El usuario no existe."

        if username not in self.historial:
            self.historial[username] = []

        self.historial[username].append(servicio)

        self.save_data()