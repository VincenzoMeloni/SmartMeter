from datetime import datetime, timedelta
import schedule
import time
from threading import Thread
from app.backend.database.db import check

FAKE_TIME = datetime(2014, 12, 11, 18, 59)

def next_fake_time():
    global FAKE_TIME
    FAKE_TIME += timedelta(minutes=1)
    return FAKE_TIME

def job_check_test():
    try:
        fake_now = next_fake_time()
        print(f"[FAKE CHECK] {fake_now} -> ",check(time=fake_now))
    except Exception as e:
        print("[TEST ERROR]", e)


def run_test(seconds=2):
    schedule.every(seconds).seconds.do(job_check_test)
    print("[TEST] Scheduler di test avviato...")

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_test():
    thread = Thread(target=run_test, daemon=True)
    thread.start()
