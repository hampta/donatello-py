
from __future__ import annotations

from datetime import datetime as Datetime
from typing import Dict, Union

from pydantic import BaseModel, Field, validator


class Donate(BaseModel):
    id: str = Field(alias="pubId")
    client_name: str = Field(alias="clientName")
    message: str = Field(alias="message")
    amount: int = Field(alias="amount")
    currency: str = Field(alias="currency")
    goal: str = Field(alias="goal", default="")
    is_published: bool = Field(alias="isPublished")
    created_at: Datetime = Field(alias="createdAt")

    @validator("created_at", pre=True)
    def validate_created_at(cls, value) -> Datetime:
        return Datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"<Donate id={self.id} client_name={self.client_name} message={self.message} amount={self.amount} currency={self.currency} goal={self.goal} is_published={self.is_published} created_at={self.created_at}>"

    def __repr__(self) -> Dict[str, Union[str, int, bool, Datetime]]:
        return f"<Donate id={self.id} client_name={self.client_name} message={self.message} amount={self.amount} currency={self.currency} goal={self.goal} is_published={self.is_published} created_at={self.created_at}>"

    def __lt__(self: Donate, other: Donate) -> bool:
        return self.amount < other.amount