import datetime
import schedule
import time
from threading import Thread
from app.backend.database.db import check,creaNotifica

def job_check():
    try:
        res = check()
        print("[CHECK]", res)

        if res["blackout"]:
            creaNotifica("blackout",f"Attenzione! Blackout Rilevato alle {datetime.datetime.now}")
        
        if res["superamento"]:
            creaNotifica("superamento",f"Attenzione! Superamento 3kW Rilevato alle {datetime.datetime.now}")
    except Exception as e:
        print("[CHECK ERROR]", e)

def run(seconds=10):
    schedule.every(seconds).seconds.do(job_check)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start():
    thread = Thread(target=run, daemon=True)
    thread.start()
