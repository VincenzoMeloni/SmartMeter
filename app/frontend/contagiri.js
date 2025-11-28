const arc = document.getElementById('livePowerArc');
const valueSpan = document.getElementById('livePowerValue');

function updateLivePower(kW) {
    valueSpan.textContent = kW.toFixed(2);

    const max = 3;
    const percent = Math.min(kW / max, 1);
    const arcLength = 203;
    arc.setAttribute('stroke-dasharray', `${arcLength * percent} ${arcLength}`);
}

setInterval(() => {
    const randomKW = Math.random() * 3;
    updateLivePower(randomKW);
}, 1000);
