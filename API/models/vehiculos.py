from sqlmodel import Field, SQLModel

class Vehiculo(SQLModel, table=True):
    vehiculo_id: int = Field(primary_key=True)
    marca: str = Field(max_length=20)
    modelo: str = Field(max_length=20)
    cliente_id:int = Field(foreign_key="client.client_id")