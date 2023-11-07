
from pydantic import BaseModel

class CardID(BaseModel):
    id: int
    love: bool