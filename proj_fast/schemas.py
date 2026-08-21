from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class InterestSchema(BaseModel):
    nome: str = Field(
    min_length=2,
    max_length=100,
    )
    email: EmailStr
    cidade: str = Field(
    min_length=2,
    max_length=100,
    )
    veiculo_id: int = Field(gt=0)
    veiculo_modelo: str = Field(
    min_length=2,
    max_length=100,
    )


class InterestPublic(InterestSchema):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )