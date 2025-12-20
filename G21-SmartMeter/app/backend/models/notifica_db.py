from dataclasses import dataclass
from datetime import datetime

@dataclass
class Notifica:
    id: int | None
    timestamp: datetime
    tipo: str
    messaggio: str
    letto: bool = False
    attivo: bool = True
