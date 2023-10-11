from __future__ import annotations

from datetime import datetime as Datetime
from typing import Dict, Union

from pydantic import BaseModel, Field, validator

from .user_donates import UserDonates


class User(BaseModel):

    nickname: str = Field(alias="nickname")
    public_id: str = Field(alias="pubId")
    page: str = Field(alias="page")
    is_active: bool = Field(alias="isActive")
    is_public: bool = Field(alias="isPublic")
    donates: UserDonates = Field(alias="donates")
    created_at: Datetime = Field(alias="createdAt")

    @validator("created_at", pre=True)
    def validate_created_at(cls, value) -> Datetime:
        return Datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"<User nickname={self.nickname} id={self.public_id} page={self.page} is_active={self.is_active} is_public={self.is_public} donates={self.donates} created_at={self.created_at}>"

    def __repr__(self) -> Dict[str, Union[str, bool, UserDonates, Datetime]]:
        return self.model_dump()
    