
# Schemat logiczny danych po stronie FastAPI

from datetime import datetime
from typing import List
from pydantic import BaseModel

class NoteSchema(BaseModel):
    id: int | None
    title: str
    content: str
    category: str  = None
    published: bool = False
    createdAt: datetime  = None
    updatedAt: datetime  = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListNoteResponse(BaseModel):
    status: str
    results: int
    notes: List[NoteSchema]