from __future__ import annotations

from typing import Dict, List, Sequence

from donatello.models.client import Client
from pydantic import BaseModel, Field


class ClientList(BaseModel):

    clients: List[Client] = Field(alias="clients", default=[])

    def __iter__(self) -> Sequence[Client]:
        for element in self.clients:
            yield element

    def __getitem__(self, item: int) -> Client:
        return self.clients[item]

    def __repr__(self) -> Dict[str, List[Client]]:
        return self.model_dump()

    def __len__(self) -> int:
        return len(self.clients)

    def __str__(self) -> str:
        return f"<ClientList clients={self.clients}>"