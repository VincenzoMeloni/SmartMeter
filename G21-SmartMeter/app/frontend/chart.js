const btn = document.getElementById('storico');
const overlay = document.getElementById('overlay');
let storicoChart = null;

btn.addEventListener('click', () => {
    openOverlay();
    caricaDatiStorico();
});

async function caricaDatiStorico() {
    const ctx = document.getElementById('storicoChart').getContext('2d');
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    let fasce_orarie = Array.from({length: 12}, (_, i) => {
        let start = String(i*2).padStart(2,'0') + ":00";
        let end = String((i*2 + 2) % 24).padStart(2,'0') + ":00";
        return `${start}-${end}`;
    });

    let somma_potenza = Array(12).fill(0);
    let count = Array(12).fill(0);

    try {
        const response = await fetch(`/sensor/giornoData`);
        const result = await response.json();

        if (result.status === "ok" && result.data && result.data.length > 0) {
            const dati = result.data;
            dati.forEach(dato => {
                const ts = new Date(dato.timestamp);
                const indice = Math.floor(ts.getHours() / 2);
                somma_potenza[indice] += dato.potenza;
                count[indice] += 1;
            });
        }
    } catch (err) {
        console.warn("Errore fetch storico:", err);
    }

    let potenza_media = somma_potenza.map((somma, i) => count[i] > 0 ? somma / count[i] : 0);

    if (storicoChart) storicoChart.destroy();

    storicoChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: fasce_orarie,
            datasets: [{
                label: 'Potenza Media Odierna (kW)',
                data: potenza_media,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true },
                tooltip: { mode: 'index' }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    ticks: {
                        stepSize: 0.5,
                        callback: value => value + " kW"
                    },
                    title: { display: true, text: 'kW' }
                },
                x: { 
                    title: { display: true, text: 'Fasce orarie' } 
                }
            }
        }
    });
}

function openOverlay() {
    overlay.classList.add('show');
    caricaDatiStorico();
}

function closeOverlay() {
    overlay.classList.remove('show');
}