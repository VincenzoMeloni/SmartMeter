# SMARTMETER
## Progetto IOT 2025/2026
---

**SmartMeter** è un progetto IOT, collocato nel contesto delle _Smart Home_, mirato alla realizzazione di un sensore che, leggendo i dati dal contatore domestico, permetta il monitoraggio energetico in tempo reale e il rilevamento di eventuali anomalie, quali blackout o superamenti della soglia di potenza.

Il progetto è stato sviluppato utilizzando _Python_ per lo sviluppo del Back-End e del Sensore. Per il Front-End è stata sviluppata una dashboard in _HTML_, _JavaScript_ e _CSS_.

Per lo sviluppo è stato utilizzato l’IDE **Visual Studio Code**

---

## INPUT

Il sensore prende in input un Dataset in formato csv così composto:

1. **timestamp**: [_datetime_] inizio del periodo di riferimento
2. **Contatore**: [_float_] valore dell'energia consumata in kWh
3. **Potenza**: [_float_] potenza istantanea prelevata in kW

---

## OUTPUT

**O1.** Il sensore effettua la lettura dei dati, inviando un file JSON al backend così formato:

    {"timestamp": "2014-12-12T00:32:00Z", "contatore": 0.614, "potenza": 0.0}

**O2.** Il backend riceve questi dati e li salva progressivamente all'interno di un file **sensor_data.csv** così strutturato:

1. **timestamp**: [_datetime_] inizio del periodo di riferimento
2. **contatore**: [_float_] valore dell'energia consumata in kWh
3. **potenza**: [_float_] potenza istantanea prelevata in kW

**O3.** Uno scheduler analizza periodicamente i dati aggiornati e genera un dizionario Python che indica la presenza di eventuali anomalie:

    {'blackout': False, 'superamento': False}

- blackout -> **True** in caso di interruzione dell’erogazione (potenza = 0 kW)
- superamento -> **True** quando la potenza supera la soglia massima (potenza >= 3 kW)

---

## GUIDA ALL'INSTALLAZIONE

### 1. Clonare Repository

Eseguire da terminale il seguente comando:

    git clone <url_repository>

### 2. Creare Ambiente Virtuale Python

Spostarsi all'interno della repository clonata:

    cd <nome_repository>/G21-SmartMeter

Lanciare il comando:

    python -m venv venv

### 3. Attivare Ambiente Virtuale

Lanciare il seguente comando da terminale:

**Windows** (cmd):

    venv\Scripts\activate

**MacOS/Linux**:

    source venv/bin/activate

### 4. Installare Le Dipendenze

All'interno dell'ambiente virtuale eseguire:

    python -m pip install -r requirements.txt

### 5. Avviare il Progetto

Aprire 2 terminali separati, entrambi con l'ambiente virtuale attivo.

All'interno del **Primo terminale** avviare il sensore digitando:

    python -m sensore.sens_main

All'interno del **Secondo terminale** avviare il server digitando:

    python main.py