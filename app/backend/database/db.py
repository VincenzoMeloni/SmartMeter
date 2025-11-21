from sqlmodel import SQLModel, Session, create_engine, select
import os
from dotenv import load_dotenv
from app.backend.models.sensore_db import SensorData

load_dotenv(dotenv_path=r"C:\INFORMATICA\Magistrale\1-ANNO\OSM-[IOT]\Progetto_IOT_residential\.env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, echo=True)
except Exception as e:
    raise RuntimeError(f"[ERRORE DB] Creazione engine fallita: {e}")

def creaDB():
    try:
        SQLModel.metadata.create_all(engine)
        print("[DB] OK.")
    except Exception as e:
        raise RuntimeError(f"[ERRORE DB] Creazione DB fallita: {e}")


def insData(sensor: SensorData):
    try:
        with Session(engine) as session:
            session.add(sensor)
            session.commit()
            session.refresh(sensor)
            return sensor
    except Exception as e:
        raise RuntimeError(f"[ERRORE DB] Inserimento dato fallito: {e}")


def getAllData():
    try:
        with Session(engine) as session:
            res = session.exec(select(SensorData)).all()
            return res
    except Exception as e:
        raise RuntimeError(f"[ERRORE DB] Lettura dati fallita: {e}")


def getUltimo():
    try:
        with Session(engine) as session:
            res = session.exec(select(SensorData).order_by(SensorData.timestamp.desc())).first()
            return res
    except Exception as e:
        raise RuntimeError(f"[ERRORE DB] Recupero ultimo dato fallito: {e}")
