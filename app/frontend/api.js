setInterval(async () => {
  try {
    const response = await fetch('/sensor/heartbeat');
    const json = await response.json();

    if (json.status !== 'ok') {
      console.warn("Backend non ha dati:", json);
      return;
    }

    window.dispatchEvent(new CustomEvent('nuoviDati', {
      detail: json.data
    }));

  } catch (err) {
    console.error("Errore fetch heartbeat:", err);
  }
}, 3000);
