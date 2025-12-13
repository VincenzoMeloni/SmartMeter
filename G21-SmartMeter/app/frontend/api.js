setInterval(async () => {
  try {
    const [hbRes, notifRes] = await Promise.all([
      fetch('/sensor/heartbeat'),
      fetch('/sensor/Notifica')
    ]);

    const hbJson = await hbRes.json();
    const notifJson = await notifRes.json();

    if (hbJson.status === 'ok') {
      window.dispatchEvent(new CustomEvent('nuoviDati', { detail: hbJson.data }));
    }

    if (notifJson.status === 'ok') {
      window.dispatchEvent(new CustomEvent('nuoveNotifiche', { detail: notifJson.data }));
    }

  } catch (err) {
    console.error("Errore fetch periodico:", err);
    window.dispatchEvent(new CustomEvent('nuoveNotifiche', { detail: [] }));
  }
}, 3000);
