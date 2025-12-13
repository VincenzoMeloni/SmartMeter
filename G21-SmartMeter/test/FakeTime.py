from datetime import datetime, timedelta
import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
indice_path = os.path.join(base_dir, "../dataset/indice.csv")

class FakeTime:
    _fake_time = datetime(2014, 12, 11, 17, 59)

    @classmethod
    def now(cls):
        return cls._fake_time

    @classmethod
    def advance(cls, seconds=0, minutes=0, hours=0):
        cls._fake_time += timedelta(seconds=seconds, minutes=minutes, hours=hours)
        return cls._fake_time

    @classmethod
    def reset(cls):
        cls._fake_time = datetime.now()
        return cls._fake_time
    
    @classmethod
    def set(cls, dt: datetime):
        cls._fake_time = dt
        return cls._fake_time
    
    @classmethod
    def load_from_csv(cls, path):
        if not os.path.exists(path):
            print(f"[FakeTime] CSV non trovato ({path}). Uso default.")
            return
        
        try:
            df = pd.read_csv(path)

            if "timestamp" not in df.columns:
                print("[FakeTime] Nessuna colonna 'timestamp'. Uso default.")
                return

            ts = pd.to_datetime(df["timestamp"].iloc[0]).replace(tzinfo=None)
            cls.set(ts)
            print(f"[FakeTime] Timestamp caricato dal CSV: {ts}")

        except Exception as e:
            print(f"[FakeTime] Errore caricamento timestamp: {e}")


FakeTime.load_from_csv(indice_path)