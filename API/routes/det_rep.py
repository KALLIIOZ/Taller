from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.det_rep import DetRep

router = APIRouter()

@router.get("/detalle/{det_rep_id}")
async def read_det_rep(det_rep_id: int, session: SessionDep):
    det_rep = session.get(DetRep, det_rep_id)
    if not det_rep:
        raise HTTPException(status_code=404, detail="DetRep not found")
    return det_rep

@router.post("/detalle")
async def create_det_rep(det_rep: DetRep, session: SessionDep):
    session.add(det_rep)
    session.commit()
    session.refresh(det_rep)
    return det_rep

@router.put("/detalle/{det_rep_id}")
async def update_det_rep(det_rep_id: int, det_rep: DetRep, session: SessionDep):
    det_rep_db = session.get(DetRep, det_rep_id)
    if not det_rep_db:
        raise HTTPException(status_code=404, detail="DetRep not found")
    det_rep_db.reparacion_id = det_rep.reparacion_id
    det_rep_db.pieza_id = det_rep.pieza_id
    det_rep_db.cantidad = det_rep.cantidad
    session.add(det_rep_db)
    session.commit()
    session.refresh(det_rep_db)
    return det_rep_db

@router.delete("/detalle/{det_rep_id}")
async def delete_det_rep(det_rep_id: int, session: SessionDep):
    det_rep = session.get(DetRep, det_rep_id)
    if not det_rep:
        raise HTTPException(status_code=404, detail="DetRep not found")
    session.delete(det_rep)
    session.commit()
    return {"message": "DetRep deleted successfully"}