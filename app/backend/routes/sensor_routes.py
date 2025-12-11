from dataclasses import asdict
from datetime import datetime
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.backend.database.db import getGiornoData, getUltimo, insData, getNotifiche, segnaNotificaLetta , deleteNotifica
from app.backend.models.sensore_db import SensorData
from app.backend.models.sensore_model import SensorModel
from test.FakeTime import FakeTime

router = APIRouter( prefix="/sensor", tags=["Sensor"])

CSV_PATH = os.path.join("dati", "sensor_data.csv")

@router.post("/heartbeat")
def heartBeat(sensor: SensorModel):
    try:
        datoDB = SensorData(timestamp=sensor.timestamp,contatore=sensor.contatore,potenza=sensor.potenza)
        insData(datoDB)
        return{"status":"ok","message": "Dato Ricevuto", "timestamp": datetime.now()}
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
        return {"status": "ok", "data": [asdict(r) for r in res]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/heartbeat")
def getLast():
    try:
        res = getUltimo()
        if res is None:
            return{"status":"None","data":"Nessun ultimo dato!"}
        return{"status":"ok","data":asdict(res)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/Notifica")
def getNotifica():
    try:
        res = getNotifiche()
        return{"status":"ok", "data": [asdict(r) for r in res]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/Notifica/{id}")
def segnaNotifica(id: int):
    try:
        res = segnaNotificaLetta(id)
        if not res:
            return {"status": "error", "message": "Notifica non trovata"}
        return{"status":"ok", "message": "Notifica segnata come letta!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@router.delete("/Notifica/{id}")
def elimina_notifica(id: int):
    try:
        res = deleteNotifica(id)
        if not res:
            return {"status": "error", "message": "Notifica non trovata"}
        return {"status": "ok", "message": "Notifica eliminata correttamente!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/download")
def scarica():
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Dati non disponibili")

    return FileResponse(
        CSV_PATH,
        media_type="text/csv",
        filename="sensor_data.csv"
    )