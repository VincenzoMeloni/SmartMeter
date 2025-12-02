from datetime import datetime, timedelta
import schedule
import time
from threading import Thread
from app.backend.database.db import check,creaNotifica
from test.FakeTime import FakeTime

def job_check_test():
    try:
        fake_now = FakeTime.now()
        FakeTime.advance(minutes=1)
        res = check(time=fake_now)
        print(f"[CHECK] {fake_now} -> ",res)

        if res["blackout"]:
            creaNotifica("blackout",f"Attenzione! Blackout Rilevato alle {fake_now}")
        
        if res["superamento"]:
            creaNotifica("superamento",f"Attenzione! Superamento 3kW Rilevato alle {fake_now}")
    except Exception as e:
        print("[TEST ERROR]", e)


def run_test(seconds=10):
    schedule.every(seconds).seconds.do(job_check_test)
    print("[TEST] Scheduler di test avviato...")

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_test():
    thread = Thread(target=run_test, daemon=True)
    thread.start()
