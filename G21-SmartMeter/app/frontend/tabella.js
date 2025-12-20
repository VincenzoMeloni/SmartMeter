const exampleData = [
        { timestamp: '2014-12-11 17:59', contatore: 3.2, potenza: 0.12, fake: "" },
        { timestamp: '2014-12-11 18:00', contatore: 3.22, potenza: 0.15, fake: true },
        { timestamp: '2014-12-11 18:01', contatore: 3.25, potenza: 0.20, fake: "" },
        { timestamp: '2014-12-11 18:02', contatore: 4.0, potenza: 3.0, fake: "" }
    ];

    const tbody = document.querySelector('#exampleTable tbody');
    exampleData.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.timestamp}</td>
            <td>${row.contatore.toFixed(3)}</td>
            <td>${row.potenza.toFixed(2)}</td>
            <td>${row.fake}</td>
        `;
        tbody.appendChild(tr);
    });