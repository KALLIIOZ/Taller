from fastapi import APIRouter, HTTPException
from API.database import SessionDep
from API.models.clientes import Client

router = APIRouter()

@router.get("/client/{client_id}")
async def read_client(client_id: int, session: SessionDep)->Client:
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/client")
async def create_client(client: Client, session: SessionDep):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.put("/client/{client_id}")
async def update_client(client_id: int, client: Client, session: SessionDep):
    client_db = session.get(Client, client_id)
    if not client_db:
        raise HTTPException(status_code=404, detail="Client not found")
    client_db.name = client.name
    client_db.rfc = client.rfc
    client_db.phone = client.phone
    client_db.user_id = client.user_id
    session.add(client_db)
    session.commit()
    session.refresh(client_db)
    return client_db

@router.delete("/client/{client_id}")
async def delete_client(client_id: int, session: SessionDep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(client)
    session.commit()
    return {"message": "Client deleted successfully"}