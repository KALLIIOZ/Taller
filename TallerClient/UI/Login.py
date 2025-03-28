import tkinter as tk
from tkinter import ttk

def Login(frame):
    ttk.Label(frame, text="Usuario").place(x=300, y=300)
    entry_user_auth = ttk.Entry(frame)
    entry_user_auth.place(x=300, y=330)

    ttk.Label(frame, text="Contraseña").place(x=300, y=360)
    entry_pass_auth = ttk.Entry(frame)
    entry_pass_auth.place(x=300, y=390)