from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class SensorData:
    id: Optional[int] = None
    timestamp: datetime = None
    contatore: float = 0.0
    potenza: float = 0.0
