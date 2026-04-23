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
Køteori er det matematiske studiet av ventelinjer og danner det teoretiske fundamentet for kapasitetsplanlegging ved lufthavner. I denne studien betraktes gatene og fjernparkeringene som "tjenesteytere" (servers), mens ankommende fly representerer "kunder" i systemet.

Sentrale prinsipper fra køteorien som er relevante for modellen inkluderer:
*   **Ankomstprosess:** Tidspunktet mellom ankomster (inter-arrival times). Selv om flyprogrammet er deterministisk, skaper forsinkelser i luften en stokastisk ankomstprosess.
*   **Tjenestetid (Service Time):** Turnaround-tiden et fly opptar en gate. Denne varierer med flytype, passasjerantall og destinasjon.
*   **Kødisiplin:** Reglene for hvem som betjenes først. Modellen bruker en kombinasjon av "First-Come, First-Served" (FCFS) og strategisk prioritering basert på flystørrelse.
*   **Littles Lov ($L = \lambda W$):** En fundamental sammenheng som sier at gjennomsnittlig antall fly i systemet er lik ankomstraten multiplisert med gjennomsnittlig ventetid.

Selv om analytiske modeller (som M/M/s-køer) kan gi raske estimater, begrenses de av flyplassens fysiske restriksjoner og gjensidig avhengige ressurser, noe som nødvendiggjør bruk av simulering.
### 2.2 Diskret-hendelse simulering (DES)
Diskret-hendelse simulering (Discrete Event Simulation - DES) er valgt som den primære modelleringsmetoden for denne studien. I motsetning til kontinuerlig simulering, hvor tilstanden endres uavbrutt over tid, fokuserer DES på spesifikke tidspunkter (hendelser) der systemets tilstand endres – for eksempel når et fly lander, en gate blir ledig, eller en buss starter transport.

Valget av DES og biblioteket SimPy i Python begrunnes med følgende faktorer:
*   **Håndtering av ressurskonflikter:** Flyplassdrift er preget av komplekse avhengigheter. Et fly som skal til en remote-stand, krever ikke bare en ledig parkeringsplass, men også en ledig buss og en tilgjengelig sjåfør samtidig. DES er spesielt sterkt på å modellere slike kø- og ressurssituasjoner.
*   **Stokastiske elementer:** Selv om flyprogrammet er fastlagt, vil faktiske ankomst- og avgangstider ofte variere. Simulering gjør det mulig å introdusere variabilitet og teste systemets robusthet.
*   **Modellering av logiske regler:** Flesland har komplekse begrensninger, som for eksempel "flex-gater" som kan skifte mellom innland og utland, men ikke begge deler samtidig. Slike betingede logiske regler er langt enklere å programmere i et DES-miljø enn å beregne med statiske matematiske modeller.

## 3. Metode
### 3.1 Forskningsdesign
Studien benytter et kvantitativt forskningsdesign basert på datasimulering. Dette designet er valgt fordi flyplassdrift er et "high-stakes" miljø hvor eksperimentering i reell drift er praktisk umulig, ekstremt kostbart og potensielt risikabelt for sikkerheten og punktligheten.

Simulering som forskningsmetode gir oss et "digitalt laboratorium" hvor vi kan:
1.  **Isolere variabler:** Vi kan endre nøyaktig én variabel (f.eks. antall busssjåfører) mens vi holder flyprogrammet og gatestrukturen helt konstant, noe som gjør det mulig å identifisere direkte årsakssammenhenger.
2.  **Stress-teste systemet:** Vi kan simulere ekstreme scenarioer, som 20% trafikkvekst, for å identifisere "knekkpunkter" i infrastrukturen før de oppstår i virkeligheten.
3.  **Dokumentere "As-Is" vs. "To-Be":** Ved først å verifisere en baseline-modell mot dagens drift, skapes et solid fundament for å evaluere effekten av fremtidige strategiske endringer.
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

**Forutsetninger og Modellantagelser:**
Siden studien kombinerer fremtidige data (Flyprogram 2026) med historiske logger (2025), er det gjort enkelte nødvendige antagelser for å kunne gjennomføre simuleringen:
*   **Rotasjonskobling:** Da det planlagte flyprogrammet for 2026 ikke eksplisitt oppgir hvilke fysiske flymaskiner som utfører hvilke ruter (fly-halenummer), er ankommende og avgående flyvninger koblet sammen manuelt basert på flyselskap, flytype og tidsvinduer. Dette danner grunnlaget for beregnet "turnaround"-tid ved gate.
*   **Representativitet:** Det legges til grunn at historiske busstider og driftstrender observert i 2025 er representative for den operasjonelle situasjonen i 2026.
*   **Fastlagt varighet:** For flyvninger med ufullstendige data eller spesielle operasjoner (som nattstopp), er det benyttet standardiserte tider for å sikre at modellen ikke stopper opp på grunn av manglende tidsverdier.
### 3.3 Simuleringsmodell (Modellbygging)
Modellen er bygget i Python ved bruk av biblioteket SimPy for diskret-hendelse simulering. Hovedlogikken i modellen følger flyets syklus fra ankomst til parkering:

**1. Logikk for Sonehåndtering og Flex-gater:**
En av de mest kritiske funksjonene i modellen er håndteringen av "flex-gater" (gate 24-32). Disse gatene kan fysisk betjene ulike soner (Innland, Schengen, Non-Schengen), men med strenge logiske begrensninger:
*   **Sone-isolering:** Dersom en flex-gate brukes av et fly fra en Non-Schengen-destinasjon, kan ikke de tilstøtende gatene i samme seksjon brukes av Schengen-fly samtidig på grunn av grensekontroll-restriksjoner.
*   **Algoritme for gatesøk:** Modellen implementerer en `finn_ledig_gate`-funksjon som søker gjennom gatene i en prioritert rekkefølge basert på flyets sone (D/I/S). Funksjonen validerer hver gate mot `sjekk_sone_konflikt`, som sikrer at ingen sikkerhetsregler brytes ved parkering.

**2. Strategisk Remote-parkering:**
For å optimalisere gate-utnyttelsen i rushtiden (Peak kl. 15:00–17:30), er det implementert en logikk som sender "små fly" (definert som fly med under 120 passasjerer) direkte til remote-parkering dersom det er ledig busskapasitet. Dette sparer terminalkapasitet for de største maskinene som krever bro-tilkobling for effektiv tømming og lasting.

**3. Ressurs-samspill (Buss og Sjåfør):**
Når et fly sendes til remote-parkering, utløses en underprosess (`busstransport`) som krever to ressurser samtidig: en buss og en sjåfør. Antall turer beregnes ut fra passasjerantallet på flyet (busskapasitet 80 pax), og modellen simulerer kjøretid mellom stand og terminal. Dette gjør det mulig å identifisere flaskehalser ikke bare i antall parkeringsplasser, men også i personellkapasitet.

### 3.4 Validering og Verifisering
For å sikre at simuleringsmodellen er pålitelig, er det gjennomført grundige prosesser for både verifisering og validering.

**Verifisering (Bygge modellen riktig):**
Verifiseringen har fokusert på å sikre at den programmerte logikken i SimPy samsvarer med de tiltenkte reglene for lufthavndriften:
*   **Trace-logger:** Det er benyttet detaljerte hendelseslogger under utviklingen for å manuelt kontrollere at fly sendes til riktige soner og at flex-gate-restriksjoner overholdes uten logiske feil.
*   **Debugger og Stress-test:** Koden er testet med ekstreme verdier (f.eks. null sjåfører eller uendelig mange fly) for å se at feilhåndteringen og kømekanismene fungerer som forventet.
*   **Modulbasert testing:** Funksjoner som `sjekk_sone_konflikt` og `finn_ledig_gate` er testet isolert for å bekrefte at de returnerer korrekte verdier under ulike parkeringsscenarioer.

**Validering (Bygge den riktige modellen):**
Valideringen skal bekrefte at modellen gir et realistisk bilde av forholdene ved Bergen Lufthavn:
*   **Face Validity:** Modellen og dens resultater er vurdert opp mot domenekunnskap og faktiske driftserfaringer. At baseline-simuleringen viser lave ventetider med to sjåfører i dagens drift, samsvarer med observasjoner fra lufthavnen.
*   **Historisk sammenligning:** Tidsbruk for busstransport og turnaround-tider i modellen er kalibrert mot de historiske bussloggene fra 2025 levert av Avinor.
*   **Baseline-sjekk:** Resultatene fra kapittel 4.2 fungerer som en endelig validering; når modellen klarer å håndtere en full dags trafikk (17. juni 2026) uten urimelige køtopper eller systemstans, anses den som tilstrekkelig nøyaktig for videre scenarieanalyse.

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
