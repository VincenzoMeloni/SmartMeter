import schedule
import time
from threading import Thread
from app.backend.database.db import check

def job_check():
    print("[CHECK] ", check())

def run():
    schedule.every(10).seconds.do(job_check)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start():
    thread = Thread(target=run, daemon=True)
    thread.start()
