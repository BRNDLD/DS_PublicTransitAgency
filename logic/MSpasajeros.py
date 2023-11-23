from logic.usuario import User
from logic.db import DbController

class PasajeroController:
    """
    Controlador para gestionar pasajeros.
    """


    def __init__(self, db_controller):
        """
        Inicializa el controlador con los archivos dados.
        """
        self.db_controller = db_controller
        self.users_data, self.historial_data, self.precios_data = self.db_controller.load_data()


    def get_usernames(self):
        """
        Get all usernames.

        :returns: List of usernames
        :rtype: list
        """
        return [user['username'] for user in self.users_data]


    def get_historial_by_username(self, username):
        """
        Get the history for a given username.

        :param username: The username to get the history for.
        :returns: The history for the given username.
        :rtype: list
        """
        return [historial for historial in self.historial_data if historial['username'] == username]


    def get_all_historial(self):
        """
        Get the history for all users.

        :returns: The history for all users.
        :rtype: dict
        """
        return {username: self.get_historial_by_username(username) for username in self.get_usernames()}


    def get_precio_by_id(self, programacion_id):
        """
        Get the price for a given programming id.

        :param programacion_id: The programming id to get the price for.
        :returns: The price for the given programming id.
        :rtype: dict
        """
        for servicio in self.precios_data:
            if servicio['id'] == programacion_id:
                return servicio
        return None


    def set_precio_by_id(self, programacion_id, precio, programacion):
        """
        Set the price for a given programming id.

        :param programacion_id: The programming id to set the price for.
        :param precio: The price to set.
        :param programacion: The programming to set the price for.
        """
        self.precios_data.append({
            "id": programacion_id,
            "tipo": programacion["tipo"],
            "placa_vehiculo": programacion["placa_vehiculo"],
            "horario": programacion["horario"],
            "vehiculo": programacion["vehiculo"],
            "ruta": programacion["ruta"],
            "precio": precio
        })
        self.db_controller.precios_collection.insert_one(self.precios_data[-1])


    def delete_precio_by_id(self, programacion_id):
        """
        Delete the price for a given programming id.

        :param programacion_id: The programming id to delete the price for.
        """
        self.precios_data = [precio for precio in self.precios_data if precio['id'] != programacion_id]
        self.db_controller.precios_collection.delete_one({'id': programacion_id})


    def add_to_historial(self, username, servicio):
        """
        Agrega un servicio al historial del usuario.

        :param username: El nombre de usuario del usuario.
        :type username: str
        :param servicio: El servicio para agregar al historial.
        :type servicio: dict
        """
        user_exists = self.db_controller.users_collection.find_one({'username': username})
        if not user_exists:
            return "El usuario no existe."

        self.historial_data.append({
            'username': username,
            'servicio': servicio
        })
        self.db_controller.historial_collection.insert_one(self.historial_data[-1])