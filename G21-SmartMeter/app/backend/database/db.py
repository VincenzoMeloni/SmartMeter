import pandas as pd
import os
from datetime import datetime, timedelta
from app.backend.models.sensore_db import SensorData
from app.backend.models.notifica_db import Notifica
from threading import Lock

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

DATI_DIR = os.path.join(BASE_DIR, "dati")
os.makedirs(DATI_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATI_DIR, "sensor_data.csv")
NOTIF_FILE = os.path.join(DATI_DIR, "notifiche.csv")

def _load_df(path, columns):
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["timestamp"])
    else:
        return pd.DataFrame({col: pd.Series(dtype="object") for col in columns})


def _save_df(df: pd.DataFrame, path):
    df.to_csv(path, index=False)

_data_lock = Lock()

def insData(sensor: SensorData):
    with _data_lock:
        df = _load_df(DATA_FILE, ["id", "timestamp", "contatore", "potenza", "fake"])

        if not df.empty:
            df = df.dropna(how='all', axis=1)

        if getattr(sensor, "timestamp", None) is None:
            if not df.empty:
                ultimo_ts = pd.to_datetime(df["timestamp"].max())
                sensor.timestamp = ultimo_ts + timedelta(seconds=70)
            else:
                sensor.timestamp = pd.Timestamp(2014, 12, 11, 17, 59, 0)
            fake = True
        else:
            fake = False

        new_id = (df["id"].max() + 1) if not df.empty else 1

        new_df = pd.DataFrame([{
            "id": int(new_id),
            "timestamp": sensor.timestamp.replace(tzinfo=None) if sensor.timestamp.tzinfo else sensor.timestamp,
            "contatore": float(sensor.contatore),
            "potenza": float(sensor.potenza),
            "fake": "true" if fake else ""
        }])

        df = pd.concat([df, new_df], ignore_index=True)
        _save_df(df, DATA_FILE)

        return SensorData(
            id=int(new_id),
            timestamp=sensor.timestamp.replace(tzinfo=None) if sensor.timestamp.tzinfo else sensor.timestamp,
            contatore=float(sensor.contatore),
            potenza=float(sensor.potenza)
        )


def _row_to_sensordata(row):
    return SensorData(
        timestamp=pd.Timestamp(row["timestamp"]).to_pydatetime(),
        contatore=float(row["contatore"]),
        potenza=float(row["potenza"])
    )

def getGiornoData(fino_a: datetime):
    df = _load_df(DATA_FILE, ["timestamp", "contatore", "potenza"])
    start = fino_a.replace(hour=0, minute=0, second=0, microsecond=0)
    df = df[(df["timestamp"] >= start) & (df["timestamp"] <= fino_a)]
    return [_row_to_sensordata(row) for _, row in df.iterrows()]

def getUltimo():
    df = _load_df(DATA_FILE, ["timestamp", "contatore", "potenza"])
    if df.empty:
        return None
    row = df.sort_values("timestamp", ascending=False).iloc[0]
    return _row_to_sensordata(row)

def getUltimi(n: int):
    df = _load_df(DATA_FILE, ["timestamp", "contatore", "potenza"])
    df = df.sort_values("timestamp", ascending=False).head(n)
    return [_row_to_sensordata(row) for _, row in df.iterrows()]

def checkBlackout(time: datetime = None):
    ultimi = getUltimi(3)

    if not ultimi:
        return True

    now = time or datetime.now()

    if now - ultimi[0].timestamp > timedelta(seconds=120):
        return True
    
    if len(ultimi) == 3 and all(d.potenza < 0.001 for d in ultimi):
        return True

    return False


def checkSuperamento():
    ultimo = getUltimo()
    return ultimo is not None and ultimo.potenza >= 3


def check(time: datetime = None):
    return {
        "blackout": bool(checkBlackout(time)),
        "superamento": bool(checkSuperamento())
    }

_notif_lock = Lock()

def creaNotifica(time: datetime, tipo: str, messaggio: str):
    with _notif_lock:
        df = _load_df(NOTIF_FILE, ["id", "timestamp", "tipo", "messaggio", "attivo", "letto"])
        new_id = int(df["id"].max() + 1) if not df.empty else 1
        new_df = pd.DataFrame([{
            "id": new_id,
            "timestamp": time,
            "tipo": tipo,
            "messaggio": messaggio,
            "attivo": True,
            "letto": False
        }])
        df = pd.concat([df, new_df], ignore_index=True)
        _save_df(df, NOTIF_FILE)
        return Notifica(id=new_id, timestamp=time, tipo=tipo, messaggio=messaggio, attivo=True, letto=False)

def chiudiNotificaAttiva(tipo: str):
    with _notif_lock:
        df = _load_df(NOTIF_FILE, ["id", "timestamp", "tipo", "messaggio", "attivo", "letto"])
        if df.empty:
            return
        df.loc[(df["tipo"] == tipo) & (df["attivo"] == True), "attivo"] = False
        _save_df(df, NOTIF_FILE)

def getNotifiche():
    df = _load_df(NOTIF_FILE, ["id", "timestamp", "tipo", "messaggio", "attivo", "letto"])
    if df.empty:
        return []
    df = df[df["id"].notna()]
    df["id"] = df["id"].astype(int)
    df["attivo"] = df["attivo"].astype(bool)
    df["letto"] = df["letto"].astype(bool)
    return [Notifica(**row) for _, row in df.iterrows()]

def segnaNotificaLetta(id: int):
    with _notif_lock:
        df = _load_df(NOTIF_FILE, ["id", "timestamp", "tipo", "messaggio", "attivo", "letto"])
        if df.empty:
            return False
        df = df[df["id"].notna()]
        df["id"] = df["id"].astype(int)
        df["attivo"] = df["attivo"].astype(bool)
        df["letto"] = df["letto"].astype(bool)
        if id not in df["id"].values:
            return False
        df.loc[df["id"] == id, "letto"] = True
        _save_df(df, NOTIF_FILE)
        return True

def deleteNotifica(id: int):
    with _notif_lock:
        df = _load_df(NOTIF_FILE, ["id", "timestamp", "tipo", "messaggio", "attivo", "letto"])
        if df.empty:
            return False
        df = df[df["id"].notna()]
        df["id"] = df["id"].astype(int)
        df["attivo"] = df["attivo"].astype(bool)
        df["letto"] = df["letto"].astype(bool)
        if id not in df["id"].values:
            return False
        df = df[df["id"] != id]
        _save_df(df, NOTIF_FILE)
        return True
