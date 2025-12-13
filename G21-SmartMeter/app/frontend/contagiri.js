const arc = document.getElementById('livePowerArc');
const valueSpan = document.getElementById('livePowerValue');
const todaySpan = document.getElementById('powerTodayValue');

function updateLivePower(kW) {
    valueSpan.textContent = kW.toFixed(2);

    const max = 3;
    const percent = Math.min(kW / max, 1);
    const arcLength = 203;
    arc.setAttribute('stroke-dasharray', `${arcLength * percent} ${arcLength}`);
}

function updateContatore(contatore) {
    todaySpan.textContent = contatore.toFixed(3);
}

window.addEventListener('nuoviDati', (e) => {
    const { contatore,potenza } = e.detail;
    updateLivePower(potenza);
    updateContatore(contatore);
});
