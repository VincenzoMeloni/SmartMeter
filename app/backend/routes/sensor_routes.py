from datetime import datetime
from fastapi import APIRouter
from app.backend.database.db import getGiornoData, getUltimo, insData
from app.backend.models.sensore_db import SensorData
from app.backend.models.sensore_model import SensorModel
from test.FakeTime import FakeTime

router = APIRouter( prefix="/sensor", tags=["Sensor"])

@router.post("/heartbeat")
def heartBeat(sensor: SensorModel):
    try:
        datoDB = SensorData(timestamp=sensor.timestamp.replace(tzinfo=None),contatore=sensor.contatore,potenza=sensor.potenza)
        insData(datoDB)
        return{"status":"ok","message": "Dato Ricevuto e memorizzato nel DB", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/giornoData")
def getGiorno(timestamp: str = None):
    try:
        if timestamp:
            ts = datetime.fromisoformat(timestamp)
        else:
            #ts = datetime.now()
            ts = FakeTime.now()
        res = getGiornoData(ts)
        if not res:
            return {"status": "None", "data": "Insieme di dati vuoto!"}
        return {"status": "ok", "data": [r.model_dump() for r in res]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/heartbeat")
def getLast():
    try:
        res = getUltimo()
        if res is None:
            return{"status":"None","data":"Nessun ultimo dato!"}
        return{"status":"ok","data":res.model_dump()}
    except Exception as e:
        return {"status": "error", "message": str(e)}