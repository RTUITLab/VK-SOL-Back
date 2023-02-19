from pydantic import BaseModel


class Ticket(BaseModel):
    _id: str | None
    user_id: str
    event_id: str
    url: str | None
    mint: str | None
    for_sell: bool | None