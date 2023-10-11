from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field


class UserDonates(BaseModel):

    total_amount: int = Field(alias="totalAmount")
    total_count: int = Field(alias="totalCount")

    def __str__(self) -> str:
        return f"<UserDonates total_amount={self.total_amount} total_count={self.total_count}>"

    def __repr__(self) -> Dict[str, int]:
        return f"<UserDonates total_amount={self.total_amount} total_count={self.total_count}>"

    def __lt__(self, other: UserDonates) -> bool:
        return self.total_amount < other.total_amount