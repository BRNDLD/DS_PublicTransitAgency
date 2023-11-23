import re
from logic.db import DbController

class User:
    """
    Class representing a user in the system.
    """

    def __init__(self, db_controller):
        """
        Initialize a User object.

        Loads user, admin and historial data from MongoDB and initializes the object.

        :returns: User object
        :rtype: User
        """
        self.db_controller = db_controller
        self.users, self.admin, self.historial = self.db_controller.load_data()

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
        return self.db_controller.authenticate(username, password)

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

    def signup(self, username, password, confirm_password):
        """
        Register a new user or admin in the system.

        :param username: The username to register.
        :type username: str
        :param password: The password for the user.
        :type password: str
        :param confirm_password: The confirmation of the password.
        :type confirm_password: str
        :returns: Success message or an error message.
        :rtype: str
        """
        username_error = self.validate_username(username)
        password_error = self.validate_password(password)

        if username_error:
            return username_error
        if password_error:
            return password_error

        if self.db_controller.username_exists(username):
            return "El nombre de usuario ya está en uso. Por favor, elige otro."
        
        if password == confirm_password:
            self.db_controller.register_user(username, password)
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
        user_exists = self.db_controller.users_collection.find_one({'username': username})
        if not user_exists:
            return "El usuario no existe."

        self.db_controller.add_to_historial(username, servicio)