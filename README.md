# Calcolatore del prezzo della nocciola IGP 🌰


Metodologia di Calcolo

Come determiniamo il prezzo minimo economicamente sostenibile.
1. La Formula

Il prezzo minimo (P_min) copre i costi di produzione, garantisce un margine di profitto e si adegua automaticamente alla classe qualitativa e al rischio climatico composito.

Passo 1: Resa_Commercializzabile = Resa_Grezza × (Percentuale_Commercializzabile / 100)

Passo 2: Costo_Base = (Costi_Produzione + Quota_Certificazione) / Resa_Commercializzabile

Passo 3: Costo_con_Margine = Costo_Base × (1 + Margine_%)

Passo 4: Correz_Qualità = lookup(Classe_Qualità)

Passo 5: Resa_Adeguata_Clima = Resa_Grezza × Coeff_Clima × Coeff_Resilienza

Passo 6: Rapporto_Adeguato = Resa_Adeguata_Clima / Resa_Riferimento

Passo 7: Premio_Rischio = lookup(Rapporto_Adeguato)

P_min = Costo_con_Margine + Correz_Qualità + Premio_Rischio

* Il prezzo finale è sempre il maggiore tra P_min e il Prezzo Minimo di Consorzio.

🚜 Variabili del Produttore (Dati Dinamici)
Inseriti dal produttore per ogni specifica partita.

    Costi di Produzione (€/ha): Spese operative per ettaro (manodopera, fertilizzanti, carburante). Esclusa la certificazione.
    Resa Grezza (kg/ha): Peso totale in guscio raccolto per ettaro.
    % Commercializzabile: Rapporto tra peso del gheriglio e peso totale del guscio (Resa di Sgusciatura), tipicamente 40–50%.
    Classe Qualitativa: La categoria specifica della partita (A, B o C).
    Coefficiente Effetto Climatico (0,5–1,5): Autovalutazione del produttore sull'impatto delle condizioni climatiche sulla resa potenziale stagionale. 1,0 = anno neutro; inferiore a 1,0 = avverso; superiore a 1,0 = favorevole.
    Coefficiente di Resilienza Aziendale (0,5–1,5): Autovalutazione della capacità dell'azienda di assorbire lo stress climatico (irrigazione, assicurazioni, riserve). 1,0 = resilienza media.

🏛️ Parametri del Consorzio (Costanti Fisse)
Definiti globalmente dall'Amministratore per garantire equità e uniformità di applicazione.

    Quota Certificazione (€/ha): Costo fisso di certificazione aggiunto a ogni ettaro (es. €25).
    % Commercializzabile Predefinita: Valore di default suggerito dal Consorzio, precompilato nel calcolatore (es. 45%).
    Margine %: Margine di profitto obbligatorio garantito al produttore (es. 10%).
    Resa di Riferimento (kg/ha): Media storica usata come benchmark per lo stress climatico (es. 1.660 kg/ha).
    Prezzo Minimo di Consorzio: Prezzo minimo assoluto di sicurezza.
    Tabelle di Correzione: Valori fissi in €/kg per bonus di qualità e premi di rischio.

2. Correzioni per la Qualità

Il prezzo viene corretto in base alla classe qualitativa della partita, per premiare l'alta uniformità e penalizzare i difetti.
Classe 	Descrizione 	Correzione
A 	Premium: alta uniformità, difetti minimi. 	+€0,20
B 	Standard: qualità commerciale conforme IGP. 	€0,00
C 	Bassa: qualità al limite, difetti elevati. 	-€0,15
3. Premio per il Rischio Climatico

Invece di basarsi esclusivamente sulla resa grezza, il sistema calcola una Resa Adeguata al Clima che combina tre segnali: il raccolto effettivo, la percezione del produttore sull'effetto climatico e la capacità di resilienza aziendale. Questo valore composito viene poi confrontato con la resa di riferimento del Consorzio per determinare il livello di rischio.

Resa_Adeguata_Clima = Resa_Grezza × Coeff_Clima × Coeff_Resilienza

Rapporto_Adeguato = Resa_Adeguata_Clima / Resa_Riferimento

🌡 Coefficiente Effetto Climatico

Autovalutazione del produttore sull'impatto climatico stagionale sulla resa potenziale. Intervallo: 0,5 (perdita estrema) a 1,5 (stagione eccezionale), passo 0,1.

🛡 Coefficiente di Resilienza Aziendale

Autovalutazione della capacità dell'azienda di assorbire lo stress climatico (irrigazione, assicurazioni, diversificazione colturale, riserve finanziarie). Intervallo: 0,5 (molto bassa) a 1,5 (molto alta), passo 0,1.
Rapporto Adeguato 	Interpretazione 	Premio di Rischio
≥ 0,90 	NORMALE 	€0,00
0,70 – 0,89 	STRESS LIEVE 	+€0,10
0,50 – 0,69 	GRAVE 	+€0,25
< 0,50 	ESTREMO 	+€0,40

* Esempio: Resa Grezza = 2.000 kg/ha, Coeff. Clima = 0,8, Coeff. Resilienza = 0,9 → Resa Adeguata al Clima = 1.440 kg/ha → Rapporto = 1.440 / 1.660 = 0,87 → Stress Lieve → +€0,10

