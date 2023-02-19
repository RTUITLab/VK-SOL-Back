from pydantic import BaseModel


class ExchangeUser(BaseModel):
    id: str
    tickets: list[str]


class Exchange(BaseModel):
    _id: str | None
    users: list[ExchangeUser]
