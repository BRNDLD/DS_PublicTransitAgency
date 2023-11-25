from logic.usuario import User
from logic.db import DbController

class PasajeroController:
    def __init__(self, db_controller: DbController):
        self.db_controller = db_controller
        self.users_data, self.historial_data, self.precios_data = self.db_controller.load_data()

    def get_usernames(self) -> list:
        return [user['username'] for user in self.users_data]

    def get_historial_by_username(self, username: str) -> list:
        return [historial for historial in self.historial_data if historial['usuario'] == username]

    def get_all_historial(self) -> dict:
        return {username: self.get_historial_by_username(username) for username in self.get_usernames()}

    def get_precio_by_id(self, programacion_id: str) -> dict:
        for servicio in self.precios_data:
            if servicio['_id']['$oid'] == programacion_id:
                return servicio
        return None

    def get_precios(self) -> list:
        return self.precios_data

    def set_precio_by_id(self, programacion_id: str, precio: float, programacion: dict):
        self.precios_data.append({
            "_id": {"$oid": programacion_id},
            "tipo": programacion["tipo"],
            "placa_vehiculo": programacion["placa_vehiculo"],
            "horario": programacion["horario"],
            "vehiculo": programacion["vehiculo"],
            "ruta": programacion["ruta"],
            "precio": precio
        })
        self.db_controller.precios_collection.insert_one(self.precios_data[-1])

    def delete_precio_by_id(self, programacion_id: str):
        self.precios_data = [precio for precio in self.precios_data if precio['_id']['$oid'] != programacion_id]
        self.db_controller.precios_collection.delete_one({'_id': {'$oid': programacion_id}})

    def add_to_historial(self, username: str, servicio: dict) -> str:
        user_exists = self.db_controller.users_collection.find_one({'username': username})
        if not user_exists:
            return "El usuario no existe."

        self.historial_data.append({
            'usuario': username,
            'viaje': {
                "tipo": servicio["tipo"],
                "placa_vehiculo": servicio["placa_vehiculo"],
                "horario": servicio["horario"],
                "vehiculo": servicio["vehiculo"],
                "ruta": servicio["ruta"],
                "precio": self.get_precio_by_id(servicio['_id']['$oid'])['precio']
            }
        })
        self.db_controller.historial_collection.insert_one(self.historial_data[-1])
