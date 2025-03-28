import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.user import User

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

    notebook.add(frame_clientes, text="Clientes")

if __name__ == "__main__":
    main()