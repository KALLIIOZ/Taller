import requests

class Clientes:
    def create_cliente(self, name: str, rfc: str, phone: str, user_id: int):
        url = "http://localhost:8000/taller/client"
        data = {
            "name": name,
            "rfc": rfc,
            "phone": phone,
            "user_id": user_id
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_cliente(self, id: int):
        url = f"http://localhost:8000/taller/client/{id}"
        response = requests.get(url)
        return response.json()

    def edit_cliente(self, id: int, name: str, rfc: str, phone: str, user_id: int):
        url =f"http://localhost:8000/taller/client/{id}"
        data = {
            "name": name,
            "rfc": rfc,
            "phone":phone,
            "user_id": user_id
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_cliente(self, id: int):
        url = f"http://localhost:8000/taller/client/{id}"
        response = requests.delete(url)
        return response.json()