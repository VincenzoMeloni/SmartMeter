from pydantic import BaseModel, Field
from datetime import datetime

class SensorModel(BaseModel):
    timestamp: datetime
    contatore: float = Field(..., ge=0)
    potenza: float = Field(..., ge=0)
