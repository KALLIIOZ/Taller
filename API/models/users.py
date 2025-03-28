from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    name: str = Field(max_length=30)
    username: str =  Field(max_length=30)
    password: str = Field(max_length=30)