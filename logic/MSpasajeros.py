import json

class PasajeroController:
    def __init__(self, users_file, historial_file):
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

    def get_usernames(self):
        return list(self.users_data.keys())

    def get_historial_by_username(self, username):
        # Cambio en esta línea para devolver una lista vacía si el usuario no tiene historial
        return self.historial_data.get(username, [])

    def get_all_historial(self):
        # Cambio en esta línea para incluir a todos los usuarios con su historial
        return {username: self.get_historial_by_username(username) for username in self.get_usernames()}