from sqlmodel import Field, SQLModel

class Pieza(SQLModel, table=True):
    pieza_id: int = Field(primary_key=True)
    descripcion: str = Field(max_length=20)
    existence: int = Field(max_length=10)
    price: float