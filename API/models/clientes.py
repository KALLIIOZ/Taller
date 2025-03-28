from sqlmodel import Field, SQLModel

class Client(SQLModel, table=True):
    client_id: int = Field(primary_key=True)
    name: str = Field(max_length=10)
    rfc: str = Field(max_length=13)
    phone: str = Field(max_length=10)
    user_id: int = Field(foreign_key="user.user_id")

