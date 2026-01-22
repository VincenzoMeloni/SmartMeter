# SMARTMETER
## Progetto IOT 2025/2026
---

**SmartMeter** è un progetto IOT, collocato nel contesto delle _Smart Home_, mirato alla realizzazione di un sensore che, leggendo i dati dal contatore domestico, permetta il monitoraggio energetico in tempo reale e il rilevamento di eventuali anomalie, quali blackout o superamenti della soglia di potenza.

Il progetto è stato sviluppato utilizzando _Python_ per lo sviluppo del Back-End e del Sensore. Per il Front-End è stata realizzata una dashboard in _HTML_, _JavaScript_ e _CSS_.

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

1. **id**: [_int_] Identificativo univoco
2. **timestamp**: [_datetime_] inizio del periodo di riferimento
3. **contatore**: [_float_] valore dell'energia consumata in kWh
4. **potenza**: [_float_] potenza istantanea prelevata in kW
5. **fake**: [_boolean_] flag che indica se il dato è stato generato dal sensore o inserito manualmente tramite una POST esterna

**O3.** Uno scheduler analizza periodicamente i dati aggiornati e genera un dizionario Python che indica la presenza di eventuali anomalie:

    {'blackout': False, 'superamento': False}

- blackout -> **True** in caso di interruzione dell’erogazione (potenza = 0 kW)
- superamento -> **True** quando la potenza supera la soglia massima (potenza >= 3 kW)

**O4.** In presenza di anomalie, il sistema registra notifiche per l’utente in un file **notifiche.csv** così formato:

1. **id**: [_int_] Identificativo univoco
2. **timestamp**: [_datetime_] istante di riferimento dell’evento
3. **tipo**: [_string_] tipologia di anomalia (Superamento o Blackout)
4. **messaggio**: [_string_] contenuto descrittivo della notifica
5. **attivo**: [_boolean_] indica se l’evento a cui si riferisce la notifica è ancora in corso
6. **letto**: [_boolean_] indica se la notifica è stata letta dall’utente

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

### 4. Creare il file .env

Copia il file di esempio _.env.example_ in _.env_

**Windows** (cmd)

    copy .env.example .env

**MacOS/Linux**:

    cp .env.example .env

### 5. Installare Le Dipendenze

All'interno dell'ambiente virtuale eseguire:

    python -m pip install -r requirements.txt

### 6. Avviare il Progetto

Aprire 2 terminali separati, entrambi con l'ambiente virtuale attivo.

All'interno del **Primo terminale** avviare il sensore digitando:

    python -m sensore.sens_main

All'interno del **Secondo terminale** avviare il server digitando:

    python main.py