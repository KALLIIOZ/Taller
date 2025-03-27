from fastapi import FastAPI, Depends, HTTPException, Query, Path
from API.routes import users, clientes
from fastapi.middleware.cors import CORSMiddleware
from API.database import create_db_and_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/taller", tags=["users"])
app.include_router(clientes.router, prefix="/taller", tags=["clientes"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()