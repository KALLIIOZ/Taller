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

def get_auth(username, password):
    user=User()
    response = user.auth(username, password)
    return response["user_id"]

# def get_vehiculos():
#     conn = sqlite3.connect('taller.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT vehiculo_id FROM vehiculo
#         ORDER BY vehiculo_id
#     """)
#     vehiculos = cursor.fetchall()
#     conn.close()
#     return [matricula[0] for matricula in vehiculos]

# def get_piezas():
#     conn = sqlite3.connect('taller.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT pieza_id, descripcion FROM pieza
#         ORDER BY descripcion
#     """)
#     piezas = cursor.fetchall()
#     conn.close()
#     return {str(id): desc for id, desc in piezas}

# def get_clients():
#     conn = sqlite3.connect('taller.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT DISTINCT c.id, c.name 
#         FROM client c
#         INNER JOIN vehiculos v ON c.id = v.cliente_id
#         ORDER BY c.name
#     """)
#     clients = cursor.fetchall()
#     conn.close()
#     return {str(id): nombre for id, nombre in clients}

# def refresh_combo(combo):
#     clients = get_clients()
#     combo['values'] = list(clients.values())
def handle_logout(notebook, frame_login):
    # Remove all tabs
    for tab in notebook.tabs():
        notebook.forget(tab)
    # Add login tab back
    notebook.add(frame_login, text="Login")

#-----------------------------------------------------------------------UI---------------------------------------------------------------------------
def logoutUI(frame, notebook, frame_login):
    logout_btn = ttk.Button(frame, text="Cerrar Sesión", command=lambda: handle_logout(notebook, frame_login))
    logout_btn.place(relx=0.5, rely=0.5, anchor='center')

def reparacionesUI(frame, username):
    rep_frame = ttk.LabelFrame(frame, text="Reparaciones")
    rep_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    ttk.Label(rep_frame, text="Folio:").grid(row=0, column=0, padx=5, pady=5)
    folio_entry = ttk.Entry(rep_frame, state='disabled')
    folio_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Vehículo:").grid(row=1, column=0, padx=5, pady=5)
    vehiculo_combo = ttk.Combobox(rep_frame, state="readonly")
    # vehiculo_combo['values'] = get_vehiculos()
    vehiculo_combo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Fecha Entrada:").grid(row=2, column=0, padx=5, pady=5)
    fecha_entrada = ttk.Entry(rep_frame)
    fecha_entrada.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Fecha Salida:").grid(row=3, column=0, padx=5, pady=5)
    fecha_salida = ttk.Entry(rep_frame)
    fecha_salida.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Usuario:").grid(row=4, column=0, padx=5, pady=5)
    usuario_label = ttk.Label(rep_frame, text=f"{username}")
    usuario_label.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Descripción:").grid(row=5, column=0, padx=5, pady=5)
    descripcion_entry = ttk.Entry(rep_frame)
    descripcion_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(rep_frame, text="Buscar Folio:").grid(row=6, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(rep_frame)
    buscar_entry.grid(row=6, column=1, padx=5, pady=5)
    
    button_frame = ttk.Frame(rep_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=10)

    nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda: Reparacion.create_rep(vehiculo_combo.get(), fecha_entrada.get(), fecha_salida.get(), descripcion_entry.get(), username))
    nuevo_btn.pack(side='left', padx=5)

    guardar_btn = ttk.Button(button_frame, text="Guardar", command=lambda: Reparacion.edit_rep(folio_entry.get(), vehiculo_combo.get(), fecha_entrada.get(), fecha_salida.get(), descripcion_entry.get()))
    guardar_btn.pack(side='left', padx=5)

    buscar_btn = ttk.Button(button_frame, text="Buscar", command=lambda: Reparacion.get_rep(buscar_entry.get()))
    buscar_btn.pack(side='left', padx=5)

    eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda: Reparacion.delete_rep(folio_entry.get()))
    eliminar_btn.pack(side='left', padx=5)

    det_frame = ttk.LabelFrame(frame, text="Detalle de Reparación")
    det_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    ttk.Label(det_frame, text="Buscar por Folio:").grid(row=0, column=0, padx=5, pady=5)
    buscar_det_entry = ttk.Entry(det_frame)
    buscar_det_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Reparación ID:").grid(row=1, column=0, padx=5, pady=5)
    rep_id_entry = ttk.Entry(det_frame)
    rep_id_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Pieza:").grid(row=2, column=0, padx=5, pady=5)
    pieza_combo = ttk.Combobox(det_frame, state="readonly")
    # piezas_dict = get_piezas()
    # pieza_combo['values'] = list(piezas_dict.values())
    pieza_combo.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
    cantidad_entry = ttk.Entry(det_frame)
    cantidad_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(det_frame, text="Descripción:").grid(row=4, column=0, padx=5, pady=5)
    desc_det_entry = ttk.Entry(det_frame)
    desc_det_entry.grid(row=4, column=1, padx=5, pady=5)

    det_button_frame = ttk.Frame(det_frame)
    det_button_frame.grid(row=5, column=0, columnspan=2, pady=10)

    agregar_btn = ttk.Button(det_button_frame, text="Agregar", command=lambda: Detalle.create_detalle(rep_id_entry.get(), pieza_combo.get(), cantidad_entry.get()))
    agregar_btn.pack(side='left', padx=5)

    guardar_det_btn = ttk.Button(det_button_frame, text="Guardar", command=lambda: Detalle.edit_detalle(rep_id_entry.get(), pieza_combo.get(), cantidad_entry.get()))
    guardar_det_btn.pack(side='left', padx=5)

    eliminar_det_btn = ttk.Button(det_button_frame, text="Eliminar", command=lambda: Detalle.delete_detalle(rep_id_entry.get()))
    eliminar_det_btn.pack(side='left', padx=5)

    frame.columnconfigure(0, weight=1)


def piezasUI(frame):
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

    ttk.Label(frame, text="Buscar ID:").grid(row=4, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=4, column=1, padx=5, pady=5)
    buscar_btn = ttk.Button(frame, text="Buscar", command=lambda:Piezas.get_pieza(buscar_entry.get()))
    buscar_btn.grid(row=4, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=5, column=0, columnspan=3, pady=20)

    nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Piezas.create_piezas(descripcion_entry.get(), precio_entry.get(), existencia_entry.get()))
    nuevo_btn.pack(side='left', padx=5)

    guardar_btn = ttk.Button(button_frame, text="Editar", command=lambda:Piezas.edit_piezas(id_entry.get(), descripcion_entry.get(), precio_entry.get(), existencia_entry.get()))
    guardar_btn.pack(side='left', padx=5)

    eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda:Piezas.delete_piezas(id_entry.get()))
    eliminar_btn.pack(side='left', padx=5)

def VehiculosUI(frame):
    ttk.Label(frame, text="Matricula:").grid(row=0, column=0, padx=5, pady=5)
    matricula_entry = ttk.Entry(frame)
    matricula_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Cliente:").grid(row=1, column=0, padx=5, pady=5)
    cliente_combo = ttk.Combobox(frame, state="readonly")
    cliente_combo.grid(row=1, column=1, padx=5, pady=5)
    #refresh_combo(cliente_combo)

    ttk.Label(frame, text="Marca:").grid(row=2, column=0, padx=5, pady=5)
    marca_entry = ttk.Entry(frame)
    marca_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Modelo:").grid(row=3, column=0, padx=5, pady=5)
    modelo_entry = ttk.Entry(frame)
    modelo_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Color:").grid(row=4, column=0, padx=5, pady=5)
    color_entry = ttk.Entry(frame)
    color_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Buscar ID:").grid(row=5, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=5, column=1, padx=5, pady=5)
    buscar_btn = ttk.Button(frame, text="Buscar")
    buscar_btn.grid(row=5, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=6, column=0, columnspan=3, pady=20)

    nuevo_btn = ttk.Button(button_frame, text="Nuevo")
    nuevo_btn.pack(side='left', padx=5)

    guardar_btn = ttk.Button(button_frame, text="Guardar")
    guardar_btn.pack(side='left', padx=5)

    editar_btn = ttk.Button(button_frame, text="Editar")
    editar_btn.pack(side='left', padx=5)

    eliminar_btn = ttk.Button(button_frame, text="Eliminar")
    eliminar_btn.pack(side='left', padx=5)

def LoginUI(frame):
    ttk.Label(frame, text="Usuario").place(x=250, y=200)
    entry_user_auth = ttk.Entry(frame)
    entry_user_auth.place(x=250, y=230)

    ttk.Label(frame, text="Contraseña").place(x=250, y=260)
    entry_pass_auth = ttk.Entry(frame)
    entry_pass_auth.place(x=250, y=290)

    return entry_user_auth, entry_pass_auth

def clientesUI(frame):
    ttk.Label(frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = ttk.Entry(frame, state='disabled')
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
    nombre_entry = ttk.Entry(frame)
    nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
    telefono_entry = ttk.Entry(frame)
    telefono_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
    email_entry = ttk.Entry(frame)
    email_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="RFC:").grid(row=4, column=0, padx=5, pady=5)
    rfc_entry = ttk.Entry(frame)
    rfc_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Usuario ID:").grid(row=5, column=0, padx=5, pady=5)
    usuario_id_entry = ttk.Entry(frame)
    usuario_id_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Buscar ID:").grid(row=6, column=0, padx=5, pady=5)
    buscar_entry = ttk.Entry(frame)
    buscar_entry.grid(row=6, column=1, padx=5, pady=5)
    buscar_btn = ttk.Button(frame, text="Buscar", command=lambda:Clientes.get_cliente(buscar_entry.get()))
    buscar_btn.grid(row=6, column=2, padx=5, pady=5)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=7, column=0, columnspan=3, pady=20)

    nuevo_btn = ttk.Button(button_frame, text="Nuevo", command=lambda:Clientes.create_cliente(nombre_entry.get(), telefono_entry.get(), email_entry.get(), rfc_entry.get(), usuario_id_entry.get()))
    nuevo_btn.pack(side='left', padx=5)

    guardar_btn = ttk.Button(button_frame, text="Editar", command=lambda:Clientes.edit_cliente(id_entry.get(), nombre_entry.get(), telefono_entry.get(), email_entry.get(), rfc_entry.get(), usuario_id_entry.get()))
    guardar_btn.pack(side='left', padx=5)

    eliminar_btn = ttk.Button(button_frame, text="Eliminar", command=lambda:Clientes.delete_cliente(id_entry.get()))
    eliminar_btn.pack(side='left', padx=5)
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
    frame_salir = ttk.Frame(notebook)

    notebook.add(frame_login, text="Login")
    user_entry, pass_entry = LoginUI(frame_login)
    clientesUI(frame_clientes)
    VehiculosUI(frame_vehiculos)
    piezasUI(frame_piezas)
    reparacionesUI(frame_reparaciones, user_entry.get())
    logoutUI(frame_salir, notebook, frame_login)
    def authenticate():
        username = user_entry.get()
        password = pass_entry.get()

        Authorize = get_auth(username, password)
        
        if Authorize == 1:
            notebook.forget(frame_login)
            notebook.add(frame_clientes, text="Clientes")
            notebook.add(frame_vehiculos, text="Vehiculos")
            notebook.add(frame_piezas, text="Piezas")
            notebook.add(frame_reparaciones, text="Reparaciones")
            notebook.add(frame_salir, text="Cerrar sesion")
        if Authorize == 2:
            notebook.forget(frame_login)
            notebook.add(frame_vehiculos, text="Vehiculos")
            notebook.add(frame_reparaciones, text="Reparaciones")
            notebook.add(frame_piezas, text="Piezas")
            notebook.add(frame_salir, text="Cerrar sesion")
    
    login_button = ttk.Button(frame_login, text="Ingresar", command=authenticate)
    login_button.place(x=272, y=350)


    notebook.pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()