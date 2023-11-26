from bson import ObjectId
from logic.usuario import User
from logic.db import DbController


class PasajeroController:
    """
    Controller class for passenger related operations.
    """


    def __init__(self, db_controller: DbController):
        """
        Initialize the PasajeroController with a DbController instance.
        """
        self.db_controller = db_controller
        self.users_data, self.historial_data, self.precios_data = self.db_controller.load_data()

    def get_usernames(self) -> list:
        """
        Get all usernames from the users data.
        """
        return [user['username'] for user in self.users_data]


    def get_historial_by_username(self, username: str) -> list:
        """
        Get the history of a user by their username.
        """
        return [historial for historial in self.historial_data if historial['usuario'] == username]


    def get_all_historial(self) -> dict:
        """
        Get the history of all users.
        """
        return {username: self.get_historial_by_username(username) for username in self.get_usernames()}


    def get_precio_by_id(self, programacion_id: str) -> dict:
        """
        Get the price by its id.
        """
        for servicio in self.precios_data:
            if str(servicio['_id']) == str(programacion_id):  # Ensure both are strings
                return servicio
        return None


    def get_precios(self) -> list:
        """
        Get all prices.
        """
        return self.precios_data


    def set_precio_by_id(self, programacion_id: str, precio: float, programacion: dict):
        """
        Set the price by its id.
        """
        precio_existente = self.get_precio_by_id(programacion_id)
        if precio_existente:
            precio_existente.update(programacion)
            precio_existente['precio'] = precio
            self.db_controller.update_precio_by_id(programacion_id, precio_existente)
        else:
            programacion['_id'] = ObjectId(programacion_id)
            programacion['precio'] = precio
            self.precios_data.append(programacion)
            self.db_controller.precios_collection.insert_one(programacion)


    def delete_precio_by_id(self, programacion_id: str):
        """
        Delete the price by its id.
        """
        self.precios_data = [precio for precio in self.precios_data if str(precio['_id']) != programacion_id]
        self.db_controller.delete_precio_by_id(programacion_id)


    def add_to_historial(self, username: str, servicio: dict) -> str:
        """
        Add a service to the user's history.
        """
        user_exists = self.db_controller.users_collection.find_one({'username': username})
        if not user_exists:
            return "El usuario no existe."

        self.historial_data.append({
            '_id': ObjectId(),
            'usuario': username,
            'viaje': {
                "tipo": servicio["tipo"],
                "placa_vehiculo": servicio["placa_vehiculo"],
                "horario": servicio["horario"],
                "vehiculo": servicio["vehiculo"],
                "ruta": servicio["ruta"],
                "precio": self.get_precio_by_id(str(servicio['_id']))['precio']
            }
        })
        self.db_controller.historial_collection.insert_one(self.historial_data[-1])


    def get_programacion_data(self) -> list:
        """
        Get all programming data.
        """
        return self.db_controller.get_programacion_data()
    