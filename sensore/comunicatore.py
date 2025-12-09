import time
import requests
import os
import schedule
from dotenv import load_dotenv
from sensore.sensore import Sensore

load_dotenv()

class Comunicatore:
    def __init__(self, sensore: Sensore):
        self.sensore = sensore
        self.backend_url = os.getenv("BACKEND_URL")

    def invia_dato(self):
        dato = self.sensore.leggi_dato()
        if dato is None:
            print("Nessun dato da inviare.")
            return

        print(f"Inviando dato al Backend: {dato}")
        try:
            r = requests.post(f"{self.backend_url}/sensor/heartbeat", json=dato, timeout=5)
            if r.status_code == requests.codes.ok:
                print(f"Status: {r.status_code} , salvo indice e timestamp")
                self.sensore.index+=1
                self.sensore.last_timestamp = dato["timestamp"]
                self.sensore.salva_indice()
            else:
                print(f"Errore dal server: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"Errore durante l'invio: {e}")

    def start(self, intervallo: int = 60):
        schedule.every(intervallo).seconds.do(self.invia_dato)

        print(f"Scheduler avviato: invio ogni {intervallo} secondi.")

        try:
            while True:
                schedule.run_pending()
                job = schedule.idle_seconds()
                if job is None or job <= 0: 
                    time.sleep(1)
                    continue
                for i in range(int(job), 0, -1):
                    print(f"Prossimo invio tra {i} s", end="\r")
                    time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("\nChiudo la comunicazione ed Interrompo lo Scheduler.")
            
