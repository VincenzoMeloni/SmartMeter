const btn = document.getElementById('storico');
const overlay = document.getElementById('overlay');
let storicoChart = null;

btn.addEventListener('click', () => {
    if (overlay.style.display === 'none' || overlay.style.display === '') {
        overlay.style.display = 'flex';
        caricaDatiStorico();
    } else {
        overlay.style.display = 'none';
    }
});

async function caricaDatiStorico() {
    const ctx = document.getElementById('storicoChart').getContext('2d');
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    let fasce_orarie = Array.from({length: 12}, (_, i) => {
        let start = String(i*2).padStart(2,'0') + ":00";
        let end = (i < 11 ? String(i*2 + 2).padStart(2,'0') : "00") + ":00";
        return `${start}-${end}`;
    });

    let potenza_per_fascia = Array(12).fill(0);

    try {
        const response = await fetch(`/sensor/giornoData`);
        const result = await response.json();

        if (result.status === "ok" && result.data && result.data.length > 0) {
            const dati = result.data;
            dati.forEach(dato => {
                const ts = new Date(dato.timestamp);
                const indice = Math.floor(ts.getHours() / 2);
                console.log(ts, indice, dato.potenza);
                potenza_per_fascia[indice] += dato.potenza;
            });
        }

    } catch (err) {
        console.warn("Errore fetch storico:", err);
    }

    if (storicoChart) storicoChart.destroy();

    storicoChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: fasce_orarie,
            datasets: [{
                label: 'Potenza giornaliera (kW)',
                data: potenza_per_fascia,
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
                    min: 0,
                    max: 3,
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