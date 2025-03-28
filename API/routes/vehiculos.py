from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.vehiculos import Vehiculo

router = APIRouter()

@router.get("/vehiculos/{vehiculo_id}")
async def read_vehiculo(vehiculo_id: int, session: SessionDep):
    vehiculo = session.get(Vehiculo, vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    return vehiculo

@router.post("/vehiculos")
async def create_vehiculo(vehiculo: Vehiculo, session: SessionDep):
    session.add(vehiculo)
    session.commit()
    session.refresh(vehiculo)
    return vehiculo

@router.put("/vehiculos/{vehiculo_id}")
async def update_vehiculo(vehiculo_id: int, vehiculo: Vehiculo, session: SessionDep):
    vehiculo_db = session.get(Vehiculo, vehiculo_id)
    if not vehiculo_db:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    vehiculo_db.marca = vehiculo.marca
    vehiculo_db.modelo = vehiculo.modelo
    vehiculo_db.color = vehiculo.color
    vehiculo_db.cliente_id = vehiculo.cliente_id
    session.add(vehiculo_db)
    session.commit()
    session.refresh(vehiculo_db)
    return vehiculo_db

@router.delete("/vehiculos/{vehiculo_id}")
async def delete_vehiculo(vehiculo_id: int, session: SessionDep):
    vehiculo = session.get(Vehiculo, vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    session.delete(vehiculo)
    session.commit()
    return {"message": "Vehiculo deleted successfully"}