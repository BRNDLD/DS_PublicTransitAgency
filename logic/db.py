from typing import List, Tuple
from pymongo import MongoClient
from bson import ObjectId
import os


class DbController:
    """
    Controller for handling database operations.
    """


    def __init__(self):
        """
        Initialize MongoDB client and collections.
        """
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["Vehiculos"]

        self.programacion_collection = db["Programacion"]
        self.users_collection = db["users"]
        self.admin_collection = db["admin"]
        self.precios_collection = db["precios"]
        self.historial_collection = db["historial"]


    def load_data(self, limit: int = 0) -> Tuple[List[dict], List[dict], List[dict]]:
        """
        Load data from users, historial, and precios collections.
        """
        users_data = list(self.users_collection.find().limit(limit))
        historial_data = list(self.historial_collection.find().limit(limit))
        precios_data = list(self.precios_collection.find().limit(limit))
        return users_data, historial_data, precios_data


    def username_exists(self, username: str) -> bool:
        """
        Check if a username exists in the users collection.
        """
        return self.users_collection.find_one({"username": username}) is not None


    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user in the users collection.
        """
        if self.username_exists(username):
            return False
        self.users_collection.insert_one({"username": username, "password": password})
        return True


    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user in the users collection.
        """
        user = self.users_collection.find_one({"username": username, "password": password})
        return user is not None


    def get_programacion(self) -> List[dict]:
        """
        Get all documents from the programacion collection.
        """
        return list(self.programacion_collection.find())


    def get_programacion_data(self, limit: int = 0) -> List[dict]:
        """
        Get documents from the programacion collection with a limit.
        """
        return list(self.programacion_collection.find().limit(limit))


    def update_precio_by_id(self, programacion_id: str, programacion: dict):
        """
        Update a document in the precios collection by id.
        """
        self.precios_collection.update_one({'_id': ObjectId(programacion_id)}, {'$set': programacion}, upsert=True)


    def delete_precio_by_id(self, programacion_id: str):
        """
        Delete a document in the precios collection by id.
        """
        self.precios_collection.delete_one({'_id': ObjectId(programacion_id)})

        
