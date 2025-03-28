from fastapi import FastAPI
from API.routes import users, clientes, vehiculos, reparacion, det_rep, piezas, auth
from fastapi.middleware.cors import CORSMiddleware
from API.database import create_db_and_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/taller", tags=["users"])
app.include_router(clientes.router, prefix="/taller", tags=["clientes"])
app.include_router(vehiculos.router, prefix="/taller", tags=["vehiculos"])
app.include_router(reparacion.router, prefix="/taller", tags=["reparacion"])
app.include_router(det_rep.router, prefix="/taller", tags=["det_rep"])
app.include_router(piezas.router, prefix="/taller", tags=["piezas"])
app.include_router(auth.router, prefix="/taller", tags=["auth"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()