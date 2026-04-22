# Optimalisering av bakkestøtte-ressurser ved Bergen Lufthavn Flesland
## En kvantitativ simuleringsstudie av gate-utnyttelse og busstransport

**Gruppe:** G03 - Bergens Beste  
**Emne:** LOG650 - Bacheloroppgave i Logistikk  
**Dato:** [Dato]

---

## Sammendrag (Abstract)
*Kort oppsummering av problemstilling, metode (simulering), viktigste funn og konklusjon.*

---

## 1. Innledning
### 1.1 Bakgrunn
Bergen Lufthavn Flesland er Norges nest største flyplass og fungerer som et kritisk knutepunkt for både nasjonal og internasjonal luftfart på Vestlandet. Med en betydelig økning i passasjertall og antall flybevegelser de siste årene, har presset på lufthavnens infrastruktur økt betraktelig. Spesielt i de daglige rushtidene (peak-perioder), hvor mange flyvninger ankommer og har avgang samtidig, oppstår det utfordringer knyttet til kapasitetsutnyttelse av gatene ved terminalen.

Når alle gatene ved terminalbygget er opptatt, må ankommende fly henvises til fjernparkering (remote stands). Dette krever bruk av busstransport for å frakte passasjerer mellom flyet og terminalen, noe som involverer ekstra ressurser i form av busser og sjåfører, og som potensielt kan føre til forsinkelser for flyselskapene og redusert komfort for passasjerene. Samtidig er det kostbart for lufthavnen å opprettholde en stor flåte av busser og personell som kun trengs i korte perioder av døgnet.

Denne studien tar for seg balansegangen mellom maksimal gate-utnyttelse og effektiv bruk av fjernparkering. Ved å bruke simulering som verktøy, kan vi undersøke hvordan ulike strategier for parkering og ressursallokering påvirker passasjerflyten og ventetider ved lufthavnen.
### 1.2 Problemstilling
Hvilken effekt har endringer i flyprogram eller ressursallokering (busser/gater) på passasjerflyten og forsinkelser?

### 1.3 Forskningsspørsmål
Studien tar sikte på å besvare følgende spørsmål gjennom simulering:
1. I hvilken grad bidrar dagens praksis med strategisk fjernparkering av mindre fly til å redusere gate-konflikter og ventetider i peak-perioder?
2. Hva er den kritiske grensen for antall busssjåfører før ventetiden for passasjerer øker markant i rushtiden?
3. Hvordan vil dagens operasjonsmodell og ressursallokering håndtere en potensiell fremtidig økning i antall flybevegelser?
### 1.4 Avgrensning
*Hva studien ikke tar for seg (f.eks. bagasjehåndtering, værforhold).*

## 2. Teoretisk Rammeverk
### 2.1 Køteori (Queueing Theory)
*Relevante prinsipper for flyplasslogistikk.*
### 2.2 Diskret-hendelse simulering (DES)
*Hvorfor SimPy er valgt som verktøy.*
### 2.3 Kapasitetsplanlegging i luftfart
*Teori om gate-utnyttelse og remote stands.*

## 3. Metode
### 3.1 Forskningsdesign
*Kvantitativ tilnærming med bruk av simulering.*
### 3.2 Datainnsamling og Datapreparering
Datagrunnlaget for studien består av tre hovedkilder levert av Avinor:
1.  **Flyprogram (Juni 2026):** Inneholder planlagte flyvninger med detaljer om flytype, setekapasitet og destinasjon (D/I/S).
2.  **Rotasjonsdata (Koblede fly):** Datasett som kobler ankommende fly med deres påfølgende avgang. Dette er kritisk for å modellere hvor lenge et fly faktisk opptar en gate ("turnaround time").
3.  **Busslogger:** Historiske data over busstransport som er brukt til å validere tidsbruk for transport mellom terminal og remote-stands.

**Datavask-prosessen (Data Cleaning):**
Rådataene ble behandlet ved hjelp av Python-biblioteket Pandas for å sikre et konsistent input-format for simuleringsmodellen (`simulation_input.csv`). Prosessen innebar følgende steg:
*   **Metadata-kobling:** Informasjon om setekapasitet og ruteinformasjon (Domestics, International, Schengen) ble koblet på rotasjonsdataene basert på flynummer.
*   **Håndtering av Nightstops:** Flyvninger som overnatter på lufthavnen ble identifisert og gitt en standardisert varighet i modellen for å sikre at de ikke blokkerer gates unødig i rushtiden.
*   **Tidsberegning:** Alle klokkeslett ble konvertert fra HH:MM-format til "minutter fra midnatt" for å forenkle tidsstyringen i SimPy-miljøet.
*   **Beregning av oppholdstid:** Faktisk tid ved gate ble beregnet som differansen mellom ankomst- og avgangstid, med håndtering av flyvninger som strekker seg over midnatt.

Resultatet av denne prosessen er et vasket datasett der hvert objekt representerer en unik "gate-hendelse" med alle nødvendige parametere for simuleringen.
### 3.3 Simuleringsmodell (Modellbygging)
Modellen er bygget i Python ved bruk av biblioteket SimPy for diskret-hendelse simulering. Hovedlogikken i modellen følger flyets syklus fra ankomst til parkering:

1.  **Agenter og Ressurser:** Flyene fungerer som agenter som krever tilgang til enten en gate eller en remote-stand (fjernparkering). Gatene er delt inn i soner (Innland, Schengen, Non-Schengen) med spesifikke begrensninger for fleksible gater (flex-gates). Busser og sjåfører er definert som begrensede ressurser som kreves ved remote-parkering.
2.  **Strategisk Remote-parkering:** For å optimalisere gate-utnyttelsen i rushtiden (Peak kl. 15:00–17:30), er det implementert en logikk som sender "små fly" (definert som fly med under 120 passasjerer) direkte til remote-parkering dersom det er ledig busskapasitet.
3.  **Prioriteringsregler:** Større fly (>120 passasjerer) prioriteres til gate. Dersom et fly ikke finner ledig gate innen 15 minutter, sendes det til remote-parkering som en sikkerhetsventil for å unngå for store forsinkelser i luften.

### 3.4 Validering og Verifisering
*Hvordan vi sikrer at modellen reflekterer virkeligheten (sammenligning med busslogger).*

## 4. Resultater og Analyse
### 4.1 Deskriptiv statistikk av rådata
*Oversikt over trafikktopper og flytyper.*

### 4.2 Simuleringsresultater (Baseline)
Simuleringen ble kjørt med data for en representativ travel dag (17. juni 2026). Baseline-scenarioet reflekterer dagens drift med 2 tilgjengelige busssjåfører og strategisk bruk av remote-parkering for små fly i rushtiden.

**Resultater fra simuleringen:**
*   **Totalt antall fly håndtert:** 141
*   **Parkering ved Gate:** 130 fly
*   **Parkering ved Remote:** 11 fly (hvorav de fleste var strategiske valg for å frigjøre gate-plass)
*   **Gjennomsnittlig ventetid:** 0,7 minutter
*   **Maksimal ventetid:** 15 minutter (forekommer i de mest kritiske trafikktoppene)
*   **Avviste fly:** 0

Analysen viser at dagens strategi med to sjåfører er tilstrekkelig for å holde ventetiden svært lav, selv med et høyt antall bevegelser. Den strategiske flyttingen av 11 fly til remote bidrar direkte til at de største flyene (f.eks. DY1849 og KL1169) kan gå direkte til gate uten forsinkelser.
### 4.3 Scenarieanalyse
*Resultater fra "Hva hvis"-scenarier (f.eks. +20% trafikk, færre busser).*
### 4.4 Statistisk signifikans
*Analyse av variasjon i resultatene over flere iterasjoner.*

## 5. Diskusjon
### 5.1 Tolkning av funn
*Hva betyr tallene for Flesland?*
### 5.2 Sammenligning med teori
*Samsvarer resultatene med køteoretiske forventninger?*
### 5.3 Praktiske implikasjoner
*Anbefalinger til Avinor.*

## 6. Konklusjon
### 6.1 Oppsummering
### 6.2 Begrensninger ved studien
### 6.3 Forslag til videre forskning

---

## Referanser
*Bruke APA 7th stil.*

---

## Vedlegg
*A: Kildekode (Python/SimPy)*  
*B: Datavask-dokumentasjon*
