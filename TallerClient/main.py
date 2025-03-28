import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.user import User
from UI.Login import Login

def get_auth(username, password):
    user=User()
    response = user.auth(username, password)
    if response["status"] == 404:
        messagebox.showerror("Error", "Usuario no encontrado")
    else:
        return response
    

def main():
    root = tk.Tk()
    root.title("Gestión de Hotel")
    root.geometry("600x600")
    notebook = ttk.Notebook(root)
    frame_login = ttk.Frame(notebook)
    frame_users = ttk.Frame(notebook)
    frame_clientes = ttk.Frame(notebook)
    frame_vehiculos = ttk.Frame(notebook)
    frame_piezas = ttk.Frame(notebook)

    notebook.add(frame_login, text="Login")
    user_entry, pass_entry = Login(frame_login)
    def authenticate():
        username = user_entry.get()
        password = pass_entry.get()

        Authorize = get_auth(username, password)
        
        if Authorize:
            notebook.add(frame_users, text="Usuarios")
            notebook.add(frame_clientes, text="Clientes")
            notebook.add(frame_vehiculos, text="Vehiculos")
            notebook.add(frame_piezas, text="Piezas")
    
    login_button = ttk.Button(frame_login, text="Ingresar", command=authenticate)
    login_button.place(x=272, y=350)


    notebook.pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()