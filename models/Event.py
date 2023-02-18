from bson import ObjectId
from pydantic import BaseModel


class Event(BaseModel):
    _id: None | ObjectId | str
    name: str
    date: str
    place: str
    cover: str | None
    user_id: str
    description: str
    amount: int     # Amount of tickets
    white_list: list[str] | None
