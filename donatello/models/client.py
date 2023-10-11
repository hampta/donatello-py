from __future__ import annotations

from typing import Dict, Union

from pydantic import BaseModel, Field


class Client(BaseModel):

    client_name: str = Field(alias="clientName")
    total_amount: int = Field(alias="totalAmount")

    def __repr__(self) -> str:
        return f"<Client client_name={self.client_name} total_amount={self.total_amount}>"

    def __str__(self) -> str:
        return f"<Client client_name={self.client_name} total_amount={self.total_amount}>"

    def __lt__(self: Client, other: Client) -> bool:
        return self.total_amount < other.total_amount