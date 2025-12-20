import schedule
import time
from threading import Thread
from app.backend.database.db import check, chiudiNotificaAttiva,creaNotifica, getNotifiche
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


def gestisci_notifica(time, tipo, condizione, messaggio):
    notifiche = getNotifiche()
    attiva = any(n.tipo == tipo and n.attivo for n in notifiche)

    if condizione and not attiva:
        creaNotifica(time, tipo, messaggio)
    elif not condizione and attiva:
        chiudiNotificaAttiva(tipo)


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

