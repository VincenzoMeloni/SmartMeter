import datetime
import schedule
import time
from threading import Thread
from app.backend.database.db import check,creaNotifica, getNotifiche, segnaNotificaLetta

def job_check_test():
    try:
        res = check()
        print(f"[CHECK] {datetime.datetime.now()} -> ",res)

        gestisci_notifica("blackout", res["blackout"], "Attenzione! Blackout Rilevato!")
        gestisci_notifica("superamento", res["superamento"], "Attenzione! Superamento 3kW Rilevato!")
    except Exception as e:
        print("[ERROR]", e)


def gestisci_notifica(tipo, condizione, messaggio):
    notifiche = getNotifiche()
    attivo = any(n.tipo == tipo and not n.letto for n in notifiche)
    if condizione and not attivo:
        creaNotifica(datetime.datetime.now(), tipo, messaggio)
    elif not condizione:
        for n in notifiche:
            if n.tipo == tipo and not n.letto:
                segnaNotificaLetta(n.id)


def run_test(seconds=3):
    schedule.every(seconds).seconds.do(job_check_test)
    print("[TEST] Scheduler avviato...")

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_test():
    try:
        thread = Thread(target=run_test, daemon=True)
        thread.start()
    except Exception as e:
        print("[START ERROR]", e)
        raise


