from typing import Literal

from pydantic import BaseModel, Field


class ClientData(BaseModel):
    age: int = Field(ge=18, le=100)
    job: str
    marital: str
    education: str
    balance: int
    housing: Literal["yes", "no"]
    loan: Literal["yes", "no"]
    campaign: int = Field(ge=1, le=100)

