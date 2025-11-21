import datetime
from fastapi import APIRouter
from app.backend.database.db import getAllData, getUltimo, insData
from app.backend.models.sensore_db import SensorData
from app.backend.models.sensore_model import SensorModel

router = APIRouter( prefix="/sensor", tags=["Sensor"])

@router.post("/heartbeat")
def heartBeat(sensor: SensorModel):
    try:
        datoDB = SensorData(**sensor.model_dump())
        insData(datoDB)
        return{"status":"ok","message": "Dato Ricevuto e memorizzato nel DB", "timestamp":datetime.now(datetime.timezone.utc)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/allData")
def getAll():
    try:
        res = getAllData()
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