from sqlmodel import Field, SQLModel

class DetRep(SQLModel, table=True):
    detrep_id: int = Field(primary_key=True)
    reparacion_id: int = Field(foreign_key="reparacion.folio")
    pieza_id: int = Field(foreign_key="pieza.pieza_id")
    cantidad: int = Field(max_length=10)