# Modelowanie danych

from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime

class Employee(BaseModel):
    id : int
    fname: str = Field(None, min_length=2, max_length=100)
    lname: str = Field(None, min_length=2, max_length=100)
    pesel : str = ""
    manager : bool = False
    acl: List[int] = []
    create_ts: Optional[datetime] = datetime.now()

    @validator("pesel")
    def pesel_validator(cls, v : str):
        if v.isdigit() and len(v)==11:
            return v
        raise ValueError("Podaj PESEL")