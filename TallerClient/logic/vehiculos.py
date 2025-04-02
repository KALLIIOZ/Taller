import requests

class Vehiculos:
    def create_vehiculos(self, marca: str, modelo: str, color: str, cliente_id: int):
        url = "http://localhost:8000/taller/vehiculos"
        data = {
            "marca": marca,
            "modelo": modelo,
            "color":color,
            "cliente_id": cliente_id
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_vehiculos(self, id: int):
        url = f"http://localhost:8000/taller/vehiculos/{id}"
        response = requests.get(url)
        return response.json()

    def edit_vehiculos(self, id: int, marca: str, modelo: str, color: str, cliente_id: int):
        url =f"http://localhost:8000/taller/vehiculos/{id}"
        data = {
            "marca": marca,
            "modelo": modelo,
            "color":color,
            "cliente_id": cliente_id
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_vehiculos(self, id: int):
        url = f"http://localhost:8000/taller/vehiculos/{id}"
        response = requests.delete(url)
        return response.json()