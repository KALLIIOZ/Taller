from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.reparacion import Reparacion

router = APIRouter()

@router.get("/reparacion/{reparacion_id}")
async def read_reparacion(reparacion_id: int, session: SessionDep)->Reparacion:
    reparacion = session.get(Reparacion, reparacion_id)
    if not reparacion:
        raise HTTPException(status_code=404, detail="Reparacion not found")
    return reparacion

@router.post("/reparacion")
async def create_reparacion(reparacion: Reparacion, session: SessionDep):
    session.add(reparacion)
    session.commit()
    session.refresh(reparacion)
    return reparacion

@router.put("/reparacion/{reparacion_id}")
async def update_reparacion(reparacion_id: int, reparacion: Reparacion, session: SessionDep):
    reparacion_db = session.get(Reparacion, reparacion_id)
    if not reparacion_db:
        raise HTTPException(status_code=404, detail="Reparacion not found")
    reparacion_db.fecha_entrada = reparacion.fecha_entrada
    reparacion_db.fecha_salida = reparacion.fecha_salida
    reparacion_db.descripcion = reparacion.descripcion
    reparacion_db.vehiculo_id = reparacion.vehiculo_id
    session.add(reparacion_db)
    session.commit()
    session.refresh(reparacion_db)
    return reparacion_db