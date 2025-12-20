from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SensorModel(BaseModel):
    timestamp: Optional[datetime] = None
    contatore: float = Field(..., ge=0)
    potenza: float = Field(..., ge=0)
