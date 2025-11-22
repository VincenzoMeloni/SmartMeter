import schedule
import time
from threading import Thread
from app.backend.database.db import check

def job_check():
    try:
        print("[CHECK]", check())
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
