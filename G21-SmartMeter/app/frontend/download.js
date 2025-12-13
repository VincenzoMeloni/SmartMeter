document.getElementById("scarica").addEventListener("click", async (e) => {
    e.preventDefault();

    try {
        const response = await fetch("/sensor/download", { method: "GET", cache: "no-store"});

        if (response.status === 404) {
            alert("I dati non sono ancora disponibili. Riprova più tardi.");
            return;
        }

        const conferma = confirm("Vuoi scaricare i log del sensore?");
        if (!conferma) return;

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "sensor_data.csv";
        a.click();

        window.URL.revokeObjectURL(url);

    } catch (err) {
        console.error(err);
        alert("Errore durante il download.");
    }
});
