from pydantic import BaseModel


class Event(BaseModel):
    _id: str | None
    name: str
    date: str
    place: str
    cover: str | None
    user_id: str
    description: str
    amount: int     # Amount of tickets
    minted: int | None
    white_list: list[str] | None
    viewed: int | None
