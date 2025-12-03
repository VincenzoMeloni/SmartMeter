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
            creaNotifica(datetime.datetime.now,"blackout","Attenzione! Blackout Rilevato!")
        
        if res["superamento"]:
            creaNotifica(datetime.datetime.now,"superamento","Attenzione! Superamento 3kW Rilevato!")
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
