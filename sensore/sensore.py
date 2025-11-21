from datetime import datetime, timezone
import random
import pandas as pd
import os

class Sensore:
    def __init__(self, csv_path: str = None,index_path = None):
        self.csv_path = csv_path
        self.index_path = index_path
        self.data = pd.read_csv(csv_path) if csv_path else None
        self.index = self.carica_indice()
    
    def leggi_dato(self):
        if self.data is not None and self.index < len(self.data):
            print("DATASET.CSV")
            row = self.data.iloc[self.index]
            return {
                "timestamp": row["timestamp"],
                "contatore": float(row["Contatore"]),
                "potenza": float(row["Potenza"])
            }
        print("Invio Dati Randomici")
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "contatore": round(random.uniform(0, 100), 2),
            "potenza": round(random.uniform(0, 5), 2)
        }

    def salva_indice(self):
        if self.index_path:
            df = pd.DataFrame({"index": [self.index]})
            df.to_csv(self.index_path, index=False)
    

    def carica_indice(self):
        if self.index_path and os.path.exists(self.index_path):
            df = pd.read_csv(self.index_path)
            if "index" in df.columns:
                return int(df["index"].iloc[0])
        return 0
