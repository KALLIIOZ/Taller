import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.user import User
from logic.clientes import Clientes
from logic.vehiculos import Vehiculos
from logic.piezas import Piezas
from logic.detalle import Detalle
from logic.reparacion import Reparacion
import sqlite3
import json, os
from datetime import datetime


def validate_dates(fecha_entrada, fecha_salida):
    try:
        entrada = datetime.strptime(fecha_entrada, '%Y-%m-%d')
        salida = datetime.strptime(fecha_salida, '%Y-%m-%d')
        
        if entrada > salida:
            messagebox.showerror("Error", "La fecha de entrada no puede ser posterior a la fecha de salida")
            return False
            
        if entrada > datetime.now():
            messagebox.showerror("Error", "La fecha de entrada no puede ser futura")
            return False
            
        return True
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
        return False

def get_auth(username, password):
    user=User()
    response = user.auth(username, password)
    return response["user_id"]

def get_vehiculos():
    conn = sqlite3.connect('./API/taller.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vehiculo_id FROM vehiculo
        ORDER BY vehiculo_id
    """)
    vehiculos = cursor.fetchall()
    conn.close()
    return [matricula[0] for matricula in vehiculos]

def get_piezas():
    conn = sqlite3.connect('./API/taller.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pieza_id, descripcion FROM pieza
        ORDER BY descripcion
    """)
    piezas = cursor.fetchall()
    conn.close()
    return {str(id): desc for id, desc in piezas}

def get_clients():
    conn = sqlite3.connect('./API/taller.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.client_id, c.name 
        FROM client c
        ORDER BY c.name
    """)
    clients = cursor.fetchall()
    conn.close()
    return {f"{id}": id for id, name in clients}

def refresh_combo_vehiculos(combo):
    try:
        clients = get_clients()
        if clients:
            combo['values'] = list(clients.keys())
    except Exception as e:
        print(f"Error refreshing combo: {e}")

def save_user_data(user_id, username):
    user_data = {
        "user_id": user_id,
        "username": username
    }
    with open('user_session.json', 'w') as f:
        json.dump(user_data, f)

def get_user_data():
    try:
        with open('user_session.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    
def configure_buttons(frame, is_admin):
    for child in frame.winfo_children():
        if isinstance(child, ttk.Frame):  # For button frames
            for button in child.winfo_children():
                if isinstance(button, ttk.Button):
                    if button['text'] in ['Eliminar', 'Editar'] and not is_admin:
                        button['state'] = 'disabled'
#-----------------------------------------------------------------------UI---------------------------------------------------------------------------

def reparacionesUI(frame, username, id):

    rep_frame = ttk.LabelFrame(frame, text="Reparaciones")
    rep_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    ttk.Label(rep_frame, text="Folio:").grid(row=0, column=0, padx=5, pady=5)
    folio_entry = ttk.Entry(rep_frame, state='disabled')
    folio_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Vehículo:").grid(row=1, column=0, padx=5, pady=5)
    vehiculo_combo = ttk.Combobox(rep_frame, state="readonly")
    vehiculo_combo['values'] = get_vehiculos()
    vehiculo_combo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Fecha Entrada:").grid(row=2, column=0, padx=5, pady=5)
    fecha_entrada = ttk.Entry(rep_frame)
    fecha_entrada.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Fecha Salida:").grid(row=3, column=0, padx=5, pady=5)
    fecha_salida = ttk.Entry(rep_frame)
    fecha_salida.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Usuario:").grid(row=4, column=0, padx=5, pady=5)
    usuario_label = ttk.Label(rep_frame, text=username)
    usuario_label.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Descripción:").grid(row=5, column=0, padx=5, pady=5)
    descripcion_entry = ttk.Entry(rep_frame)
    descripcion_entry.grid(row=5, column=1, padx=5, pady=5)

    def search_reparacion():
        reparacion_data = Reparacion.get_rep(buscar_entry, buscar_entry.get())
        print(reparacion_data)
        if reparacion_data:
            folio_entry.configure(state='normal')
            folio_entry.delete(0, tk.END)
            folio_entry.insert(0, reparacion_data["folio"])
            folio_entry.configure(state='disabled')
            
            vehiculo_combo.set(reparacion_data["vehiculo"])
            
            fecha_entrada.delete(0, tk.END)
            fecha_entrada.insert(0, reparacion_data["fecha_entrada"])
            
            fecha_salida.delete(0, tk.END)
            fecha_salida.insert(0, reparacion_data["fecha_salida"])
            
            descripcion_entry.delete(0, tk.END)
            descripcion_entry.insert(0, reparacion_data["descripcion"])
    def search_detalle():
        detalle_data = Detalle.get_detalle(buscar_det_entry, buscar_det_entry.get())
        if detalle_data:
            rep_id_entry.delete(0, tk.END)
            rep_id_entry.insert(0, detalle_data["detrep_id"])
            
            pieza_combo.set(detalle_data["pieza_id"])
            
            cantidad_entry.delete(0, tk.END)
            cantidad_entry.insert(0, detalle_data["cantidad"])
            
            desc_det_entry.delete(0, tk.END)
            desc_det_entry.insert(0, detalle_data["descripcion"])

    ttk.Label(rep_frame, text="Buscar Folio:").grid(row=6, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(rep_frame)
    buscar_entry.grid(row=6, column=1, padx=5, pady=5)
    
    button_frame = ttk.Frame(rep_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=10)


    if id == 1:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", 
            command=lambda: create_rep_validated())
        nuevo_btn.pack(side='left', padx=5)

        guardar_btn = ttk.Button(button_frame, text="Editar", 
            command=lambda: edit_rep_validated())
        guardar_btn.pack(side='left', padx=5)


        eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda: Reparacion.delete_rep(folio_entry.get()))
        eliminar_btn.pack(side='left', padx=5)
    else:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", 
            command=lambda: create_rep_validated())
        nuevo_btn.pack(side='left', padx=5)
    
    buscar_btn = ttk.Button(button_frame, text="Buscar", command=search_reparacion())  # Quitar lambda y get_rep
    buscar_btn.pack(side='left', padx=5)

    def create_rep_validated():
        if validate_dates(fecha_entrada.get(), fecha_salida.get()):
            Reparacion.create_rep(folio_entry, 
                                fecha_entrada.get(), 
                                fecha_salida.get(), 
                                descripcion_entry.get(),
                                vehiculo_combo.get())

    def edit_rep_validated():
        if validate_dates(fecha_entrada.get(), fecha_salida.get()):
            Reparacion.edit_rep(folio_entry,
                              fecha_entrada.get(),
                              fecha_salida.get(),
                              descripcion_entry.get(),
                              vehiculo_combo.get())



    det_frame = ttk.LabelFrame(frame, text="Detalle de Reparación")
    det_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    ttk.Label(det_frame, text="Buscar por Folio:").grid(row=0, column=0, padx=5, pady=5)
    buscar_det_entry = ttk.Entry(det_frame)
    buscar_det_entry.grid(row=0, column=1, padx=5, pady=5)
    buscar_det_btn = ttk.Button(det_frame, text="Buscar", command=search_detalle())  # Agregar botón faltante
    buscar_det_btn.grid(row=0, column=2, padx=5, pady=5)

    ttk.Label(det_frame, text="Reparación ID:").grid(row=1, column=0, padx=5, pady=5)
    rep_id_entry = ttk.Entry(det_frame)
    rep_id_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Pieza:").grid(row=2, column=0, padx=5, pady=5)
    pieza_combo = ttk.Combobox(det_frame, state="readonly")
    piezas_dict = get_piezas()
    pieza_combo['values'] = list(piezas_dict.values())
    pieza_combo.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
    cantidad_entry = ttk.Entry(det_frame)
    cantidad_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Descripción:").grid(row=4, column=0, padx=5, pady=5)
    desc_det_entry = ttk.Entry(det_frame)
    desc_det_entry.grid(row=4, column=1, padx=5, pady=5)

    det_button_frame = ttk.Frame(det_frame)
    det_button_frame.grid(row=5, column=0, columnspan=2, pady=10)

    if id == 1:
        agregar_btn = ttk.Button(det_button_frame, text="Nuevo", command=lambda: Detalle.create_detalle(rep_id_entry.get(), pieza_combo.get(), cantidad_entry.get()))
        agregar_btn.pack(side='left', padx=5)

        guardar_det_btn = ttk.Button(det_button_frame, text="Editar", command=lambda: Detalle.edit_detalle(rep_id_entry.get(), pieza_combo.get(), cantidad_entry.get()))
        guardar_det_btn.pack(side='left', padx=5)

        eliminar_det_btn = ttk.Button(det_button_frame, text="Eliminar", command=lambda: Detalle.delete_detalle(rep_id_entry.get()))
        eliminar_det_btn.pack(side='left', padx=5)
    else:
        agregar_btn = ttk.Button(det_button_frame, text="Nuevo", command=lambda: Detalle.create_detalle(rep_id_entry.get(), pieza_combo.get(), cantidad_entry.get()))
        agregar_btn.pack(side='left', padx=5)


    frame.columnconfigure(0, weight=1)


def piezasUI(frame, id):
    ttk.Label(frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = ttk.Entry(frame, state='disabled')
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
    descripcion_entry = ttk.Entry(frame)
    descripcion_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
    precio_entry = ttk.Entry(frame)
    precio_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Existencia:").grid(row=3, column=0, padx=5, pady=5)
    existencia_entry = ttk.Entry(frame)
    existencia_entry.grid(row=3, column=1, padx=5, pady=5)

    def search_pieza():
        pieza_data = Piezas.get_piezas(buscar_entry, buscar_entry.get())
        if pieza_data:
            id_entry.configure(state='normal')
            id_entry.delete(0, tk.END)
            id_entry.insert(0, pieza_data["pieza_id"])
            id_entry.configure(state='disabled')
            
            descripcion_entry.delete(0, tk.END)
            descripcion_entry.insert(0, pieza_data["descripcion"])
            
            precio_entry.delete(0, tk.END)
            precio_entry.insert(0, pieza_data["price"])
            
            existencia_entry.delete(0, tk.END)
            existencia_entry.insert(0, pieza_data["existence"])

    ttk.Label(frame, text="Buscar ID:").grid(row=4, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=4, column=1, padx=5, pady=5)
    buscar_btn = ttk.Button(frame, text="Buscar", command=lambda:search_pieza())
    buscar_btn.grid(row=4, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=5, column=0, columnspan=3, pady=20)
    if id == 1:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Piezas.create_piezas(id_entry, descripcion_entry.get(), existencia_entry.get(), precio_entry.get()))
        nuevo_btn.pack(side='left', padx=5)

        guardar_btn = ttk.Button(button_frame, text="Editar", command=lambda:Piezas.edit_piezas(id_entry.get(), descripcion_entry.get(), precio_entry.get(), existencia_entry.get()))
        guardar_btn.pack(side='left', padx=5)

        eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda:Piezas.delete_piezas(id_entry, id_entry.get()))
        eliminar_btn.pack(side='left', padx=5)
    else:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Piezas.create_piezas(descripcion_entry.get(), precio_entry.get(), existencia_entry.get()))
        nuevo_btn.pack(side='left', padx=5)

def VehiculosUI(frame, id):
    ttk.Label(frame, text="Matricula:").grid(row=0, column=0, padx=5, pady=5)
    matricula_entry = ttk.Entry(frame, state='disabled')
    matricula_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Cliente:").grid(row=1, column=0, padx=5, pady=5)
    cliente_combo = ttk.Combobox(frame, state="readonly")
    cliente_combo.grid(row=1, column=1, padx=5, pady=5)
    refresh_combo_vehiculos(cliente_combo)  # Usa la nueva función específica

    ttk.Label(frame, text="Marca:").grid(row=2, column=0, padx=5, pady=5)
    marca_entry = ttk.Entry(frame)
    marca_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Modelo:").grid(row=3, column=0, padx=5, pady=5)
    modelo_entry = ttk.Entry(frame)
    modelo_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Color:").grid(row=4, column=0, padx=5, pady=5)
    color_entry = ttk.Entry(frame)
    color_entry.grid(row=4, column=1, padx=5, pady=5)

    def search_vehiculo():
        vehiculo_data = Vehiculos.get_vehiculos(buscar_entry, buscar_entry.get())
        if vehiculo_data:
            matricula_entry.configure(state='normal')
            matricula_entry.delete(0, tk.END)
            matricula_entry.insert(0, vehiculo_data["vehiculo_id"])
            matricula_entry.configure(state='disabled')
            
            cliente_combo.set(vehiculo_data["cliente_id"])
            
            marca_entry.delete(0, tk.END)
            marca_entry.insert(0, vehiculo_data["marca"])
            
            modelo_entry.delete(0, tk.END)
            modelo_entry.insert(0, vehiculo_data["modelo"])
            
            color_entry.delete(0, tk.END)
            color_entry.insert(0, vehiculo_data["color"])

    ttk.Label(frame, text="Buscar ID:").grid(row=5, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=5, column=1, padx=5, pady=5)
    buscar_btn = ttk.Button(frame, text="Buscar", command=lambda:search_vehiculo())
    buscar_btn.grid(row=5, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=6, column=0, columnspan=3, pady=20)
    if id == 1:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Vehiculos.create_vehiculos(matricula_entry, marca_entry.get(), modelo_entry.get(), color_entry.get(), cliente_combo.get()))
        nuevo_btn.pack(side='left', padx=5)

        editar_btn = ttk.Button(button_frame, text="Editar", command=lambda:Vehiculos.edit_vehiculos(matricula_entry, marca_entry.get(), modelo_entry.get(), color_entry.get(), cliente_combo.get()))
        editar_btn.pack(side='left', padx=5)

        eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda:Vehiculos.delete_vehiculos(matricula_entry.get()))
        eliminar_btn.pack(side='left', padx=5)
    else:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Vehiculos.create_vehiculos(matricula_entry, marca_entry.get(), modelo_entry.get(), color_entry.get(), cliente_combo.get()))
        nuevo_btn.pack(side='left', padx=5)

def LoginUI(frame):
    ttk.Label(frame, text="Usuario").place(x=250, y=200)
    entry_user_auth = ttk.Entry(frame)
    entry_user_auth.place(x=250, y=230)

    ttk.Label(frame, text="Contraseña").place(x=250, y=260)
    entry_pass_auth = ttk.Entry(frame)
    entry_pass_auth.place(x=250, y=290)

    return entry_user_auth, entry_pass_auth

def clientesUI(frame, id):
    ttk.Label(frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = ttk.Entry(frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
    nombre_entry = ttk.Entry(frame)
    nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    telefono_entry = ttk.Entry(frame)
    telefono_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="RFC:").grid(row=4, column=0, padx=5, pady=5)
    rfc_entry = ttk.Entry(frame)
    rfc_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Usuario ID:").grid(row=5, column=0, padx=5, pady=5)
    usuario_id_entry = ttk.Entry(frame)
    usuario_id_entry.insert(0, id)
    usuario_id_entry.configure(state='disabled')
    usuario_id_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Buscar ID:").grid(row=6, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=6, column=1, padx=5, pady=5)

    def search_client(id):
        client_data = Clientes.get_cliente(id, id)
        if client_data:
            id_entry.configure(state='normal')
            id_entry.delete(0, tk.END)
            id_entry.insert(0, client_data["client_id"])
            id_entry.configure(state='disabled')
            
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, client_data["name"])
            
            telefono_entry.delete(0, tk.END)
            telefono_entry.insert(0, client_data["phone"])
            
            rfc_entry.delete(0, tk.END)
            rfc_entry.insert(0, client_data["rfc"])
            
            usuario_id_entry.configure(state='normal')
            usuario_id_entry.delete(0, tk.END)
            usuario_id_entry.insert(0, client_data["user_id"])

    
    buscar_btn = ttk.Button(frame, text="Buscar", command=lambda:search_client(buscar_entry.get()))
    buscar_btn.grid(row=6, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=7, column=0, columnspan=3, pady=20)
    if id == 1:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Clientes.create_cliente(id_entry,nombre_entry.get(), rfc_entry.get(), telefono_entry.get(), usuario_id_entry.get()))
        nuevo_btn.pack(side='left', padx=5)

        guardar_btn = ttk.Button(button_frame, text="Editar", command=lambda:Clientes.edit_cliente(id_entry, nombre_entry.get(), rfc_entry.get(), telefono_entry.get(), usuario_id_entry.get()))
        guardar_btn.pack(side='left', padx=5)

        eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda:Clientes.delete_cliente(id_entry, id_entry.get()))
        eliminar_btn.pack(side='left', padx=5)
    else:
        nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Clientes.create_cliente(id_entry, nombre_entry.get(), telefono_entry.get(),  rfc_entry.get(), usuario_id_entry.get()))
        nuevo_btn.pack(side='left', padx=5)
#-----------------------------------------------------------------------UI---------------------------------------------------------------------------


def main():
    root = tk.Tk()
    root.title("Gestión de Hotel")
    root.geometry("600x600")
    notebook = ttk.Notebook(root)
    frame_login = ttk.Frame(notebook)
    frame_clientes = ttk.Frame(notebook)
    frame_vehiculos = ttk.Frame(notebook)
    frame_reparaciones = ttk.Frame(notebook)
    frame_piezas = ttk.Frame(notebook)

    notebook.add(frame_login, text="Login")
    user_entry, pass_entry = LoginUI(frame_login)
    def authenticate():
        username = user_entry.get()
        password = pass_entry.get()

        Authorize = get_auth(username, password)
        save_user_data(Authorize, username)
        user_data = get_user_data()
        user_name = user_data.get("username")
        userID = user_data.get("user_id")
        if Authorize == 1:
            notebook.forget(frame_login)
            notebook.add(frame_clientes, text="Clientes")
            notebook.add(frame_vehiculos, text="Vehiculos")
            notebook.add(frame_piezas, text="Piezas")
            notebook.add(frame_reparaciones, text="Reparaciones")
            clientesUI(frame_clientes, userID)
            VehiculosUI(frame_vehiculos, userID)
            piezasUI(frame_piezas, userID)
            reparacionesUI(frame_reparaciones, user_name, userID)
        if Authorize == 2:
            notebook.forget(frame_login)
            notebook.add(frame_reparaciones, text="Reparaciones")
            reparacionesUI(frame_reparaciones, user_name, userID)
        if Authorize == 3:
            notebook.forget(frame_login)
            notebook.add(frame_clientes, text="Clientes")
            notebook.add(frame_vehiculos, text="Vehiculos")
            clientesUI(frame_clientes, userID)
            VehiculosUI(frame_vehiculos, userID)
    
    login_button = ttk.Button(frame_login, text="Ingresar", command=authenticate)
    login_button.place(x=272, y=350)


    notebook.pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()