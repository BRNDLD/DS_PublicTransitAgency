from typing import List, Tuple
from pymongo import MongoClient

# Conexión con la base de datos MongoDB
client = MongoClient("mongodb+srv://publictransit:qwerty32@pta.bueovsa.mongodb.net/?tls=true")

if client is not None:
    db = client["Vehiculos"]
    collection_programacion = db["Programacion"]
    collection_rutas = db["Rutas"]
    collection_vehiculos = db["vehiculos"]  
    collection_users = db["users"]
    collection_admin = db["admin"]
    collection_precios = db["precios"]
    collection_historial = db["historial"]

    class DbController:
        def __init__(self):
            self.users_collection = collection_users
            self.historial_collection = collection_historial
            self.precios_collection = collection_precios

        def load_data(self, limit: int = 0) -> Tuple[List[dict], List[dict], List[dict]]:
            """
            Carga los datos de usuario, historial y precios de las colecciones MongoDB.

            :param limit: Límite opcional para el número de documentos a devolver
            :returns: Tupla que contiene los datos de usuario, historial y precios
            :rtype: Tuple[List[dict], List[dict], List[dict]]
            """
            users_data = list(self.users_collection.find().limit(limit))
            historial_data = list(self.historial_collection.find().limit(limit))
            precios_data = list(self.precios_collection.find().limit(limit))
            return users_data, historial_data, precios_data

        def username_exists(self, username: str) -> bool:
            """
            Comprueba si un nombre de usuario ya existe en la base de datos.

            :param username: El nombre de usuario a comprobar
            :returns: True si el nombre de usuario existe, False en caso contrario
            :rtype: bool
            """
            return self.users_collection.find_one({"username": username}) is not None

        def register_user(self, username: str, password: str, code: str):
            """
            Registra un nuevo usuario en la base de datos.

            :param username: El nombre de usuario del nuevo usuario
            :type username: str
            :param password: La contraseña del nuevo usuario
            :type password: str
            """
            self.users_collection.insert_one({"username": username, "password": password})
    