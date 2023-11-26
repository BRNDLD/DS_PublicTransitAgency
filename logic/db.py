from typing import List, Tuple
from pymongo import MongoClient
from bson import ObjectId

class DbController:
    def __init__(self):
        client = MongoClient("mongodb+srv://publictransit:qwerty32@pta.bueovsa.mongodb.net/?tls=true")
        db = client["Vehiculos"]

        self.programacion_collection = db["Programacion"]
        self.users_collection = db["users"]
        self.admin_collection = db["admin"]
        self.precios_collection = db["precios"]
        self.historial_collection = db["historial"]

    def load_data(self, limit: int = 0) -> Tuple[List[dict], List[dict], List[dict]]:
        users_data = list(self.users_collection.find().limit(limit))
        historial_data = list(self.historial_collection.find().limit(limit))
        precios_data = list(self.precios_collection.find().limit(limit))
        return users_data, historial_data, precios_data

    def username_exists(self, username: str) -> bool:
        return self.users_collection.find_one({"username": username}) is not None

    def register_user(self, username: str, password: str) -> bool:
        if self.username_exists(username):
            return False
        self.users_collection.insert_one({"username": username, "password": password})
        return True

    def authenticate(self, username: str, password: str) -> bool:
        user = self.users_collection.find_one({"username": username, "password": password})
        return user is not None

    def get_programacion(self) -> List[dict]:
        return list(self.programacion_collection.find())
    
    def get_programacion_data(self, limit: int = 0) -> List[dict]:
        return list(self.programacion_collection.find().limit(limit))

    def update_precio_by_id(self, programacion_id: str, programacion: dict):
        self.precios_collection.update_one({'_id': ObjectId(programacion_id)}, {'$set': programacion}, upsert=True)

    def delete_precio_by_id(self, programacion_id: str):
        self.precios_collection.delete_one({'_id': ObjectId(programacion_id)})

        