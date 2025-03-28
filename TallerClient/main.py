import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.user import User


def get_auth(user, password):
    user=User()
    response = user.auth(user, password)
    if response["status"] == 404:
        messagebox.showerror("Error", "Usuario no encontrado")
    else:
        return response
    

def Login(frame):
    ttk.Label(frame, text="Usuario").place(x=250, y=200)
    entry_user_auth = ttk.Entry(frame)
    entry_user_auth.place(x=250, y=230)

    ttk.Label(frame, text="Contraseña").place(x=250, y=260)
    entry_pass_auth = ttk.Entry(frame)
    entry_pass_auth.place(x=250, y=290)

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
    Authorize = Login(frame_login)
    if Authorize:
        notebook.add(frame_users, text="Usuarios")
        notebook.add(frame_clientes, text="Clientes")
        notebook.add(frame_vehiculos, text="Vehiculos")
        notebook.add(frame_piezas, text="Piezas")

    notebook.pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()