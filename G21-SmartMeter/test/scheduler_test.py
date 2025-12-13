import schedule
import time
from threading import Thread
from app.backend.database.db import check,creaNotifica, getNotifiche, segnaNotificaLetta
from test.FakeTime import FakeTime

def job_check_test():
    try:
        fake_now = FakeTime.now()
        FakeTime.advance(minutes=1)
        res = check(time=fake_now)
        print(f"[CHECK] {fake_now} -> ",res)

        gestisci_notifica(fake_now,"blackout", res["blackout"], "Attenzione! Blackout Rilevato!")
        gestisci_notifica(fake_now,"superamento", res["superamento"], "Attenzione! Superamento 3kW Rilevato!")
    except Exception as e:
        print("[TEST ERROR]", e)


def gestisci_notifica(fake_now, tipo, condizione, messaggio):
    notifiche = getNotifiche()
    attivo = any(n.tipo == tipo and not n.letto for n in notifiche)
    if condizione and not attivo:
        creaNotifica(fake_now, tipo, messaggio)
    elif not condizione:
        for n in notifiche:
            if n.tipo == tipo and not n.letto:
                segnaNotificaLetta(n.id)


def run_test(seconds=3):
    schedule.every(seconds).seconds.do(job_check_test)
    print("[TEST] Scheduler di test avviato...")

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_test():
    try:
        thread = Thread(target=run_test, daemon=True)
        thread.start()
    except Exception as e:
        print("[START TEST ERROR]", e)
        raise

