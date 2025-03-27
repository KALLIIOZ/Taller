from sqlmodel import Field, SQLModel

class Reparacion(SQLModel, table=True):
    folio: int = Field(primary_key=True)
    fecha_entrada: str = Field(max_length=10)
    fecha_salida: str = Field(max_length=10)
    descripcion: str = Field(max_length=500)
    vehiculo_id: int = Field(foreign_key="vehiculo.vehiculo_id")