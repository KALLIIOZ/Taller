import requests

class Piezas:
    def create_piezas(self, descripcion: str, existence: int, price: float):
        url = "http://localhost:8000/taller/piezas"
        data = {
            "descripcion": descripcion,
            "existence":existence,
            "price":price,
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_piezas(self, id: int):
        url = f"http://localhost:8000/taller/piezas/{id}"
        response = requests.get(url)
        return response.json()

    def edit_piezas(self, id: int, descripcion: str, existence: int, price: float):
        url =f"http://localhost:8000/taller/piezas/{id}"
        data = {
            "descripcion": descripcion,
            "existence":existence,
            "price":price,
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_piezas(self, id: int):
        url = f"http://localhost:8000/taller/piezas/{id}"
        response = requests.delete(url)
        return response.json()