from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.piezas import Pieza

router = APIRouter()

@router.get("/piezas/{pieza_id}")
async def read_pieza(pieza_id: int, session: SessionDep):
    pieza = session.get(Pieza, pieza_id)
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza not found")
    return pieza

@router.post("/piezas")
async def create_pieza(pieza: Pieza, session: SessionDep):
    session.add(pieza)
    session.commit()
    session.refresh(pieza)
    return pieza

@router.put("/piezas/{pieza_id}")
async def update_pieza(pieza_id: int, pieza: Pieza, session: SessionDep):
    pieza_db = session.get(Pieza, pieza_id)
    if not pieza_db:
        raise HTTPException(status_code=404, detail="Pieza not found")
    pieza_db.descripcion = pieza.descripcion
    pieza_db.existence = pieza.existence
    pieza_db.price = pieza.price
    session.add(pieza_db)
    session.commit()
    session.refresh(pieza_db)
    return pieza_db

@router.delete("/piezas/{pieza_id}")
async def delete_pieza(pieza_id: int, session: SessionDep):
    pieza = session.get(Pieza, pieza_id)
    if not pieza:
        raise HTTPException(status_code=404, detail="Pieza not found")
    session.delete(pieza)
    session.commit()
    return {"message": "Pieza deleted successfully"}