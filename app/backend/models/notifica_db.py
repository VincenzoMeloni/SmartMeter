import datetime
from sqlmodel import SQLModel, Field

class Notifica(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime.datetime
    tipo: str
    messaggio: str
    letto: bool = Field(default=False)
