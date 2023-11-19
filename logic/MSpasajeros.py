import json
from logic.usuario import User

class PasajeroController:
    def __init__(self, users_file, historial_file, precios_file):
        self.users_file = users_file
        self.historial_file = historial_file
        self.precios_file = precios_file
        self.users_data, self.historial_data, self.precios_data = self.load_data()

    def load_data(self):
        """
        Load user, historial and precios data from JSON files.

        :returns: Tuple containing user, historial and precios data
        :rtype: Tuple[dict, dict, dict]
        """
        with open(self.users_file, 'r') as users_file:
            users_data = json.load(users_file)
        with open(self.historial_file, 'r') as historial_file:
            historial_data = json.load(historial_file)
        with open(self.precios_file, 'r') as precios_file:
            precios_data = json.load(precios_file)
        return users_data, historial_data, precios_data

    def save_data(self):
        """
        Save user, historial and precios data to JSON files.
        """
        with open(self.users_file, 'w') as users_file:
            json.dump(self.users_data, users_file)
        with open(self.historial_file, 'w') as historial_file:
            json.dump(self.historial_data, historial_file)
        with open(self.precios_file, 'w') as precios_file:
            json.dump(self.precios_data, precios_file)

        try:
            with open(users_file, "r") as users_json:
                self.users_data = json.load(users_json)
        except Exception as e:
            print(f"Error cargando {users_file}: {e}")
            self.users_data = {}

        try:
            with open(historial_file, "r") as historial_json:
                self.historial_data = json.load(historial_json)
        except Exception as e:
            print(f"Error cargando {historial_file}: {e}")
            self.historial_data = {}

        try:
            with open(precios_file, "r") as precios_json:
                self.precios_data = json.load(precios_json)
        except Exception as e:
            print(f"Error cargando {precios_file}: {e}")
            self.precios_data = {}

        self.precios_file = precios_file

    def get_usernames(self):
        return list(self.users_data.keys())

    def get_historial_by_username(self, username):
        return self.historial_data.get(username, [])

    def get_all_historial(self):
        return {username: self.get_historial_by_username(username) for username in self.get_usernames()}

    def get_precio_by_id(self, programacion_id):
    # Buscar el servicio con el programacion_id dado
        for servicio in self.precios_data.values():
            if servicio['id'] == programacion_id:
                return servicio

    # Si no se encuentra el servicio, devolver None
        return None

    def set_precio_by_id(self, programacion_id, precio, programacion):
        self.precios_data[str(programacion_id)] = {
            "id": programacion_id,
            "tipo": programacion["tipo"],
            "placa_vehiculo": programacion["placa_vehiculo"],
            "horario": programacion["horario"],
            "vehiculo": programacion["vehiculo"],
            "ruta": programacion["ruta"],
            "precio": precio
        }

        with open(self.precios_file, "w") as precios_json:
            json.dump(self.precios_data, precios_json)

    def delete_precio_by_id(self, programacion_id):
        if str(programacion_id) in self.precios_data:
            del self.precios_data[str(programacion_id)]

            with open(self.precios_file, "w") as precios_json:
                json.dump(self.precios_data, precios_json)

    def add_to_historial(self, username, servicio):
        """
        Add a service to the user's history.

        :param username: The username of the user.
        :type username: str
        :param servicio: The service to add to the history.
        :type servicio: dict
        """
        # Asegúrate de que el usuario existe
        if username not in self.users_data:
            return "El usuario no existe."

        # Asegúrate de que el usuario tiene un historial
        if username not in self.historial_data:
            self.historial_data[username] = []

        # Agrega el servicio al historial
        self.historial_data[username].append(servicio)

        # Guarda los datos
        self.save_data()