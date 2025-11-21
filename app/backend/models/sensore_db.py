import datetime
from sqlmodel import SQLModel, Field

class SensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime.datetime
    contatore: float
    potenza: float