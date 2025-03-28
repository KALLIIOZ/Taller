import requests
import json


class User:
    def auth(self, username: str, password: str):
        url = "http://localhost:8000/taller/auth"
        data = {"username": username, "password": password}
        response = requests.request("GET", url, params=data)
        return response.json()

    def create_user(self, name: str, username: str, password: str):
        url = "http://localhost:8000/taller/user"
        data = {"name": name,"username": username, "password": password}
        response = requests.post(url, json=data)
        return response.json()

    def get_user(self, id: int):
        url = f"http://localhost:8000/taller/user/"
        data={"id":id}
        response = requests.get(url, json=data)
        return response.json()
    
    def edit_user(self, id: int, name: str, username: str, password: str):
        url = f"http://localhost:8000/taller/user/{id}"
        data = {"name": name,"username": username, "password": password}
        response = requests.put(url, json=data)
        return response.json()

    def delete_user(self, id: int):
        url = f"http://localhost:8000/taller/user/{id}"
        response = requests.delete(url)
        return response.json()