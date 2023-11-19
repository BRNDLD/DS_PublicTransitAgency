import json

class PasajeroController:
    def __init__(self, users_file, historial_file, precios_file):
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
        return self.precios_data.get(str(programacion_id), {}).get("precio")

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