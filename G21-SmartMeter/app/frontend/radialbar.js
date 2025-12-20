document.addEventListener("DOMContentLoaded", function() {
    var maxPower = 3;

    var options = {
        chart: {
            type: 'radialBar',
            height: '100%',
            width: '100%',
            animations: { enabled: true, easing: 'easeinout', speed: 800 }
        },
        series: [ 0 ],
        plotOptions: {
            radialBar: {
                startAngle: -90,
                endAngle: 90,
                hollow: { size: '60%' },
                track: { background: '#eee' },
                dataLabels: {
                    name: { show: true, fontSize: '14px', offsetY: -10, color: '#333' },
                    value: {
                        show: true,
                        fontSize: '25px',
                        fontWeight: 'bold',
                        formatter: function(val) {return ((val / 100) * maxPower).toFixed(2) + " kW";}
                    }
                }
            }
        },
        fill: { colors: ['brown'] },
        labels: ['Consumo Live']
    };

    var chart = new ApexCharts(document.querySelector("#livePowerChart"), options);
    chart.render();

    window.addEventListener('nuoviDati', (e) => {
        const {contatore, potenza} = e.detail;
        chart.updateSeries([ (potenza / maxPower) * 100 ]);
        updateContatore(contatore);
    });

});

function updateContatore(contatore) {
    const todaySpan = document.getElementById('powerTodayValue');
    todaySpan.textContent = contatore.toFixed(3);
}