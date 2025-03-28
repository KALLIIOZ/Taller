import tkinter as tk
from tkinter import ttk, messagebox

def Login(frame):
    ttk.Label(frame, text="Usuario").place(x=250, y=200)
    entry_user_auth = ttk.Entry(frame)
    entry_user_auth.place(x=250, y=230)

    ttk.Label(frame, text="Contraseña").place(x=250, y=260)
    entry_pass_auth = ttk.Entry(frame)
    entry_pass_auth.place(x=250, y=290)

    return entry_user_auth, entry_pass_auth