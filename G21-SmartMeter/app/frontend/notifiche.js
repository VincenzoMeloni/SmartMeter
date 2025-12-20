document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.getElementById("OverlayNotifiche");
  const btnNotifiche = document.getElementById("notifiche");
  const container = document.querySelector('#OverlayNotifiche .notifiche-content');

  if (!container) {
    console.error("Container notifiche non trovato!");
    return;
  }

  btnNotifiche.addEventListener("click", (e) => {
    e.stopPropagation();
    overlay.classList.toggle("aperto");
  });

  document.addEventListener("click", (e) => {
    if (overlay.classList.contains("aperto") && !overlay.contains(e.target) && e.target !== btnNotifiche) {
      overlay.classList.remove("aperto");
    }
  });

  window.addEventListener('nuoveNotifiche', (e) => {
    const notifiche = e.detail;

    notifiche.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    if (!notifiche || notifiche.length === 0) {
      container.innerHTML = "<div class='notifica-messaggio' style='text-align: center;'>Nessuna Notifica da Mostrare</div>";
      aggiornaBadge([]);
      return;
    }

    container.innerHTML = notifiche.map(n => `
      <div class="notifica ${n.letto ? '' : 'non-letto'}" data-id="${n.id}" onclick="segnaNotificaLetta(${n.id})">
        <div class="notifica-text">
          <div class="notifica-messaggio">${n.messaggio}</div>
          <div class="notifica-footer">
            <div class="notifica-timestamp">${formattaData(n.timestamp)}</div>
            <button class="notifica-delete" onclick="eliminaNotifica(${n.id})">
              <i class="fa fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    `).join("");
    aggiornaBadge(notifiche);
  });

});

function formattaData(ts) {
  if (!ts) return "";
  return new Date(ts).toLocaleString("it-IT");
}

async function eliminaNotifica(id) {
  try {
    const res = await fetch(`/sensor/Notifica/${id}`, { method: 'DELETE' });
    const data = await res.json();

    if (data.status === "ok") {
      const notificaElem = document.querySelector(`.notifica[data-id='${id}']`);
      if (notificaElem) notificaElem.remove();

    } else {
      console.error("Errore eliminazione notifica:", data.message);
    }
  } catch (err) {
    console.error("Errore nella fetch di eliminazione:", err);
  }
}

async function segnaNotificaLetta(id) {
  try {
    const res = await fetch(`/sensor/Notifica/${id}`, { method: 'POST' });
    const data = await res.json();

    if (data.status === 'ok') {
      const notificaElem = document.querySelector(`.notifica[data-id="${id}"]`);
      if (notificaElem) {
        notificaElem.classList.remove('non-letto');
      }
    } else {
      console.error("Errore segnando notifica:", data.message);
    }
  } catch (err) {
    console.error("Errore fetch segnare notifica:", err);
  }
}

function aggiornaBadge(notifiche) {
  const badge = document.getElementById("badgeNotifiche");
  const nonLette = notifiche.filter(n => !n.letto).length;

  if (nonLette > 0) {
    badge.textContent = nonLette;
    badge.style.display = "flex";
  } else {
    badge.style.display = "none";
  }
}
