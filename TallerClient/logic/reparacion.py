import requests

class Reparacion:
    def create_rep(self, fecha_e: str, fecha_s: str, descripcion: str, vehiculo_id: int):
        url = "http://localhost:8000/taller/reparacion"
        data = {
            "fecha_entrada": fecha_e,
            "fecha_salida":fecha_s,
            "descripcion":descripcion,
            "vehiculo_id": vehiculo_id
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_rep(self, id: int):
        url = f"http://localhost:8000/taller/reparacion/{id}"
        response = requests.get(url)
        return response.json()

    def edit_rep(self, id: int, fecha_e: str, fecha_s: str, descripcion: str, vehiculo_id: int):
        url =f"http://localhost:8000/taller/reparacion/{id}"
        data = {
            "fecha_entrada": fecha_e,
            "fecha_salida":fecha_s,
            "descripcion":descripcion,
            "vehiculo_id": vehiculo_id
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_rep(self, id: int):
        url = f"http://localhost:8000/taller/reparacion/{id}"
        response = requests.delete(url)
        return response.json()