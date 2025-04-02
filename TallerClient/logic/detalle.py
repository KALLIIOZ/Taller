import requests

class Detalle:
    def create_detalle(self, reparacion_id: int, pieza_id: int, cantidad: int):
        url = "http://localhost:8000/taller/detalle"
        data = {
            "reparacion_id": reparacion_id,
            "pieza_id":pieza_id,
            "cantidad":cantidad,
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_detalle(self, id: int):
        url = f"http://localhost:8000/taller/detalle/{id}"
        response = requests.get(url)
        return response.json()

    def edit_detalle(self, id: int, reparacion_id: int, pieza_id: int, cantidad: int):
        url =f"http://localhost:8000/taller/detalle/{id}"
        data = {
            "reparacion_id": reparacion_id,
            "pieza_id":pieza_id,
            "cantidad":cantidad,
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_detalle(self, id: int):
        url = f"http://localhost:8000/taller/detalle/{id}"
        response = requests.delete(url)
        return response.json()