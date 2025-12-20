document.addEventListener("DOMContentLoaded", function() {
    var maxPower = 3;
    var data = [];
    var maxPoints = 50;

    var optionsHeartbeat = {
        chart: {
            type: 'line',
            height: 150,
            animations: { enabled: true, easing: 'linear', dynamicAnimation: { speed: 3500 } },
            toolbar: { show: false },
            zoom: { enabled: false }
        },
        series: [{ name: 'Consumo Live', data: data }],
        colors: ['brown'],
        xaxis: { type: 'datetime',
            labels: {
                datetimeUTC: false
            }
         },
        yaxis: {
            min: 0,
            max: maxPower,
            labels: { formatter: function(val){ return val.toFixed(1); } }
        },
        stroke: { curve: 'smooth' },
        tooltip: {
            shared: false,
            custom: function({ series, seriesIndex, dataPointIndex }) {
                const value = series[seriesIndex][dataPointIndex];
                return `<div style="padding:5px; font-family: Helvetica, Arial, sans-serif;">
                            <strong>Consumo Live:</strong> ${value.toString()} kW
                        </div>`;
            }
        }
    };

    var heartbeatChart = new ApexCharts(document.querySelector("#realtimeChart"), optionsHeartbeat);
    heartbeatChart.render();

    window.addEventListener('nuoviDati', (e) => {
        const {timestamp, potenza} = e.detail;
        data.push({x: new Date(timestamp).getTime(), y: potenza});
        if(data.length > maxPoints) data.shift();
        heartbeatChart.updateSeries([{ data: data }]); 
    });
});
