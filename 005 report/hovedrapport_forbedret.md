# Optimalisering av bakkestøtte-ressurser ved Bergen Lufthavn Flesland
## En kvantitativ simuleringsstudie av gate-utnyttelse og busstransport

**Gruppe:** G03 - Bergens Beste  
**Emne:** LOG650 - Bacheloroppgave i Logistikk  
**Dato:** 30. april 2026

---

## Sammendrag
Denne rapporten undersøker kapasitetsutnyttelsen av gater og behovet for busstransport ved Bergen Lufthavn Flesland gjennom diskret-hendelse simulering (DES) i Python med SimPy. Problemstillingen fokuserer på balansen mellom maksimal utnyttelse av terminalnære gater og effektiv bruk av fjernparkering (remote stands) i peak-perioder. Ved å analysere et planlagt flyprogram for en travel sommerdag i 2026, indikerer studien at dagens operasjonsmodell med aktiv gate-styring og to tilgjengelige busssjåfører i rushtiden er robust. Resultatene viser en gjennomsnittlig ventetid på under ett minutt, selv ved høy trafikkbelastning. Scenarioanalyser viser imidlertid at systemet er sårbart ved bemanningsreduksjon til én sjåfør, da dette fjerner den operative bufferen som trengs for å håndtere uforutsette avvik. Videre indikerer simuleringen at lufthavnen har kapasitet til å håndtere en trafikkvekst på inntil 20 % i rushtiden uten vesentlig økning i ventetid, forutsatt at dagens ressursallokering opprettholdes. Rapporten konkluderer med at strategisk bruk av fjernparkering for mindre flymaskiner er en kritisk suksessfaktor for effektiv drift ved Flesland.

---

## 1. Innledning
### 1.1 Bakgrunn
Bergen Lufthavn Flesland er Norges nest største flyplass og fungerer som et kritisk knutepunkt for både nasjonal og internasjonal luftfart på Vestlandet. Med en betydelig økning i passasjertall og antall flybevegelser de siste årene, har presset på lufthavnens infrastruktur økt betraktelig. Spesielt i de daglige rushtidene (peak-perioder), hvor mange flyvninger ankommer og har avgang samtidig, oppstår det utfordringer knyttet til kapasitetsutnyttelse av gatene ved terminalen.

Når alle gatene ved terminalbygget er opptatt, må ankommende fly henvises til fjernparkering (remote stands). Dette krever bruk av busstransport for å frakte passasjerer mellom flyet og terminalen, noe som involverer ekstra ressurser i form av busser og sjåfører, og som potensielt kan føre til forsinkelser for flyselskapene og redusert komfort for passasjerene. Samtidig er det kostbart for lufthavnen å opprettholde en stor flåte av busser og personell som kun trengs i korte perioder av døgnet.

Denne studien tar for seg balansegangen mellom maksimal gate-utnyttelse og effektiv bruk av fjernparkering. Ved å bruke simulering som verktøy, kan vi undersøke hvordan ulike strategier for parkering og ressursallokering påvirker passasjerflyten og ventetider ved lufthavnen.

### 1.2 Problemstilling
Hvordan kan Bergen Lufthavn Flesland håndtere flest mulig samtidige ankomster i peak-perioder gjennom optimal bruk av gater, remote stands, busser og busssjåfører, uten at ventetid før gate overstiger et definert terskelnivå?

Problemstillingen konkretiseres ved å analysere hvor mange ankomster systemet kan håndtere i et definert peak-vindu før kø, ventetid eller ressursutnyttelse indikerer at kapasiteten er presset. Studien vurderer særlig hvordan strategisk bruk av remote stands og dimensjonering av busssjåførkapasitet påvirker ventetid, gateutnyttelse og operativ robusthet.

I denne rapporten defineres systemet som operativt robust dersom gjennomsnittlig ventetid før gate er lav og maksimal ventetid ikke overstiger et akseptabelt terskelnivå i de analyserte scenarioene. Et praktisk terskelnivå kan for eksempel settes til 15 minutter maksimal ventetid eller til en valgt 95-persentil dersom modellen senere utvides med stokastiske simuleringer.

### 1.3 Forskningsspørsmål
Studien tar sikte på å besvare følgende spørsmål gjennom simulering:
1. I hvilken grad bidrar strategisk fjernparkering av mindre fly til å redusere gatekonflikter og ventetid i peak-perioder?
2. Hvor følsomt er systemet for endringer i antall tilgjengelige busssjåfører?
3. Hvordan påvirkes ventetid, remote-bruk og gateutnyttelse av økt trafikk i peak-perioden?
4. Hvilke ressurser fremstår som de mest kritiske flaskehalsene: terminalgater, remote stands, busser eller busssjåfører?

### 1.4 Avgrensning
For å sikre en fokusert analyse av gate- og busskapasitet, er følgende faktorer holdt utenfor studiens omfang:

*   **Bagasjehåndtering:** Studien ser kun på flyets bevegelse og passasjertransport mellom fly og terminal. Flaskehalser i bagasjesystemet eller tilgang på bagasjevogner er ikke modellert.
*   **Teknisk pålitelighet og vedlikehold:** Modellen forutsetter 100 % oppetid på fysisk infrastruktur (broer, busser) og ser bort fra uforutsette tekniske feil eller vedlikeholdsstans i simuleringsperioden.
*   **Fysisk trafikkavvikling på taksebaner:** Kjøretider for busser er basert på historiske gjennomsnittstall og inkluderer ikke sanntidsinteraksjon med flytrafikk eller andre kjøretøy på flyplassområdet som kan skape lokale forsinkelser.
*   **Ground Handling (Bakketjenester):** Det forutsettes at eksterne tjenester som catering, fylling av drivstoff og teknisk vedlikehold utføres innenfor flyets planlagte turnaround-tid. Tilgang på personell fra handling-agenter (f.eks. Widerøe Ground Handling eller Aviator) er antatt å være ubegrenset.
*   **Værforhold:** Simuleringen tar utgangspunkt i normale operative forhold (sommerprogram). Ekstremvær som krever avising (de-icing) eller snørydding, som ville endret både turnaround-tider og banekapasitet, er ikke inkludert.
*   **Sikkerhetskontroll og landside-kapasitet:** Studien fokuserer på "airside"-operasjoner. Kapasitetsutfordringer i terminalens avgangshall, sikkerhetskontroll eller passkontroll er ikke en del av modellen.

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

### 3.4 Matematisk modellformulering
For å gjøre simuleringsmodellen etterprøvbar, beskrives den også som en forenklet matematisk kapasitetsmodell. Den matematiske formuleringen brukes ikke til å erstatte DES-modellen, men til å tydeliggjøre hvilke beslutningsvariabler, måleparametere og begrensninger som ligger til grunn for analysen.

**Indekser og mengder:**
*   $i \in I$: flybevegelser i datasettet
*   $g \in G$: tilgjengelige terminalgater
*   $r \in R$: remote stands
*   $t \in T$: tidsperioder i simuleringshorisonten

**Sentrale parametere:**
*   $S_i$: planlagt ankomsttid for fly $i$
*   $P_i$: passasjerkapasitet eller estimert passasjerantall for fly $i$
*   $C_b$: kapasitet per buss, målt i passasjerer
*   $B$: antall tilgjengelige busser
*   $D$: antall tilgjengelige busssjåfører
*   $\tau_i$: forventet oppholdstid eller turnaround-tid for fly $i$
*   $W_{max}$: akseptabel terskelverdi for ventetid før gate eller remote stand

**Beslutningsvariabler:**
*   $x_{ig}=1$ dersom fly $i$ tildeles gate $g$, ellers $0$
*   $y_{ir}=1$ dersom fly $i$ tildeles remote stand $r$, ellers $0$
*   $d_t$: antall busssjåfører tilgjengelig i periode $t$

Hovedmålet er å håndtere flest mulig samtidige ankomster innenfor eksisterende infrastruktur, samtidig som ventetiden holdes under et definert terskelnivå. Dette kan uttrykkes som:

$$
\max A
$$

der $A$ er antall ankomster som kan håndteres i peak-perioden uten at ventetidskravet brytes. En sentral kapasitetsbegrensning er:

$$
\bar{W}_q \leq W_{max}
$$

der $\bar{W}_q$ er gjennomsnittlig ventetid før gate eller remote stand. Gjennomsnittlig ventetid beregnes som:

$$
\bar{W}_q = \frac{1}{n}\sum_{i=1}^{n} W_{q,i}
$$

der $W_{q,i}$ er ventetiden for fly $i$, og $n$ er antall fly i simuleringen. Maksimal ventetid beregnes som:

$$
W_{q,max} = \max(W_{q,1}, W_{q,2}, ..., W_{q,n})
$$

For fly som sendes til remote stand, beregnes behovet for bussturer som:

$$
b_i = \left\lceil \frac{P_i}{C_b} \right\rceil
$$

der $b_i$ er antall nødvendige bussturer for fly $i$. Formelen gjør det mulig å koble passasjerantall direkte til belastning på buss- og sjåførressursene.

Ressursutnyttelse beregnes for hver sentral ressurs $r$ som:

$$
\rho_r = \frac{B_r}{T_r}
$$

der $B_r$ er samlet opptatt tid for ressurs $r$, og $T_r$ er samlet tilgjengelig tid. En verdi nær 1 indikerer høy utnyttelse og mulig flaskehals. For eksempel kan $\rho_r$ beregnes separat for terminalgater, remote stands, busser og busssjåfører.

Dersom modellen senere utvides med tilfeldige forsinkelser, kan faktisk ankomsttid modelleres som:

$$
T_i^{ankomst} = S_i + \varepsilon_i
$$

der $\varepsilon_i$ er et tilfeldig avvik fra planlagt ankomsttid. Dette muliggjør Monte Carlo-simulering og beregning av variasjon, persentiler og konfidensintervaller for ventetid.

### 3.5 Validering og Verifisering
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
*   **Baseline-sjekk:** Resultatene fra kapittel 4.2 fungerer som en plausibilitetssjekk; når modellen håndterer en full dags trafikk (17. juni 2026) uten urimelige køtopper eller systemstans, styrker dette tilliten til at modellen er egnet for videre scenarieanalyse.

For å gjøre valideringen mer etterprøvbar bør den suppleres med en eksplisitt sammenligning mellom historiske data og simulert baseline. En mulig struktur er vist nedenfor. Tallene bør fylles inn dersom datagrunnlaget tillater det.

| Måleparameter | Historisk/observert verdi | Simulert baseline | Avvik |
|---|---:|---:|---:|
| Gjennomsnittlig busstur | Ikke beregnet | Ikke beregnet | Ikke beregnet |
| Antall remote-operasjoner | Ikke beregnet | 11 | Ikke beregnet |
| Gjennomsnittlig ventetid før gate | Ikke beregnet | 0,7 min | Ikke beregnet |
| Maksimal ventetid før gate | Ikke beregnet | 15 min | Ikke beregnet |

Avvik kan beregnes som:

$$
\text{Avvik} = \frac{\text{Simulert verdi} - \text{Historisk verdi}}{\text{Historisk verdi}} \cdot 100\%
$$

### 3.6 Planlagte tester og scenariooppsett
For å styrke analysens etterprøvbarhet bør scenarioene struktureres som kontrollerte eksperimenter der én sentral parameter endres om gangen. I den nåværende rapporten er baseline, redusert bemanning og trafikkvekst analysert. For videre modellkjøringer anbefales et mer systematisk testoppsett:

| Test | Parameter som endres | Formål |
|---|---|---|
| Baseline | Dagens ressursnivå | Referansepunkt for sammenligning |
| Sjåførkapasitet | 0, 1, 2 og 3 sjåfører | Finne kritisk bemanningsnivå |
| Trafikkvekst | +10 %, +20 % og +30 % i peak | Identifisere kapasitetsgrense |
| Remote-strategi | Strategisk remote av/på | Måle effekt av aktiv gate-styring |
| Busstid | -20 %, normal, +20 % | Teste følsomhet for transporttid |
| Busskapasitet | 60, 70, 80 og 90 passasjerer | Teste effekt av kapasitet per buss |
| Stokastiske forsinkelser | Lav, middels og høy forsinkelsesvariasjon | Teste robusthet under realistiske avvik |

Dersom stokastiske forsinkelser inkluderes, bør hvert scenario kjøres mange ganger, for eksempel 100 eller 500 replikasjoner. Da kan resultatene presenteres med gjennomsnitt, standardavvik og 95 % konfidensintervall:

$$
CI_{95\%} = \bar{x} \pm 1.96 \cdot \frac{s}{\sqrt{n}}
$$

der $\bar{x}$ er gjennomsnittlig resultat fra simuleringene, $s$ er standardavviket og $n$ er antall replikasjoner. Dette vil gi et sterkere grunnlag for å vurdere om forskjeller mellom scenarioer er robuste eller bare skyldes tilfeldige variasjoner.

## 4. Resultater og Analyse
### 4.1 Deskriptiv statistikk av rådata
Før simuleringen ble gjennomført, ble det vaskede datasettet for den valgte testdagen (17. juni 2026) analysert for å forstå trafikkbelastningen. Denne dagen representerer en travel sommerdag med totalt **141 flybevegelser** (rotasjoner).

**Fordeling av destinasjonssoner (D/I/S):**
*   **Innland (D):** 97 flyvninger (68,8%)
*   **Schengen (S):** 38 flyvninger (27,0%)
*   **Non-Schengen (I):** 6 flyvninger (4,2%)

Dominansen av innenlandstrafikk stiller store krav til gatene i den rene innlandssonen, mens de fleksible gatene i Schengen/Non-Schengen-området må håndtere en betydelig andel av de resterende flyvningene.

**Flystørrelse og kapasitet:**
*   **Små fly (<120 seter):** 81 flyvninger
*   **Store fly (>=120 seter):** 60 flyvninger
*   **Gjennomsnittlig setekapasitet:** 124,7 seter per fly

Det høye antallet små fly (over 57%) bekrefter potensialet for den strategiske fjernparkeringen i rushtiden, da disse flyene utgjør en betydelig volummasse som ellers ville blokkert gate-kapasitet for de større maskinene. De fleste av disse små maskinene er Widerøe- og mindre SAS-flyvninger som er godt egnet for busstransport.

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

Tabell 1 oppsummerer de simulerte hovedresultatene fra scenarioene som hittil er gjennomført. Tabellen bør utvides med 95-persentil, gateutnyttelse og sjåførutnyttelse dersom disse målene hentes ut fra simuleringsmodellen.

| Scenario | Sjåfører | Vekst | Remote-strat | Stokastisk | Fly | Gate | Remote | Gj.sn. ventetid | Maks ventetid |
|:---|---:|---:|:---|:---|---:|---:|---:|---:|---:|
| Baseline | 2 | 0 % | PÅ | NEI | 141 | 130 | 11 | 0,71 min | 15,0 min |
| 0 sjåfører | 0 | 0 % | PÅ | NEI | 141 | 141 | 0 | 2,16 min | 60,0 min |
| 1 sjåfør | 1 | 0 % | PÅ | NEI | 141 | 133 | 8 | 0,92 min | 15,0 min |
| 3 sjåfører | 3 | 0 % | PÅ | NEI | 141 | 127 | 14 | 0,71 min | 15,0 min |
| Remote AV | 2 | 0 % | AV | NEI | 141 | 136 | 5 | 1,21 min | 15,0 min |
| Vekst +10 % | 2 | 10 % | PÅ | NEI | 143 | 132 | 11 | 0,70 min | 15,0 min |
| Vekst +20 % | 2 | 20 % | PÅ | NEI | 146 | 133 | 13 | 0,96 min | 15,0 min |
| Vekst +30 % | 2 | 30 % | PÅ | NEI | 149 | 135 | 14 | 0,97 min | 15,0 min |
| Kjøretid +20% | 2 | 0 % | PÅ | NEI | 141 | 131 | 10 | 0,71 min | 15,0 min |
| Stokastisk (snitt) | 2 | 0 % | PÅ | JA | 141 | 128 | 13 | 0,68 min | 15,4 min |


### 4.3 Scenarieanalyse
For å besvare forskningsspørsmålene om systemets robusthet og kritiske grenser, ble det gjennomført to målrettede scenarieanalyser.

**Scenario 1: Redusert bemanning (Stress-test av sjåførkapasitet)**
I dette scenariet ble antall tilgjengelige busssjåfører redusert fra to til én på den travleste dagen i datasettet (17. juni). Hensikten var å identifisere hvor avhengig den strategiske gate-planleggingen er av kontinuerlig busskapasitet.

*Resultater:*

*   **Gjennomsnittlig ventetid:** Økte fra 0,71 til 0,92 minutter.
*   **Antall strategiske remote-parkeringer:** Redusert fra 11 til 8.
*   **Maksimal ventetid:** Vedvarte på 15 minutter.

*Analyse av sårbarhet:*
Ekstrem-testen med **null sjåfører** viser en gjennomsnittlig ventetid på 2,16 minutter, men en maksimal ventetid på hele 60 minutter. Dette understreker at uten busstransport vil enkelte fly bli stående og blokkere for andre i svært lang tid, noe som skaper en uakseptabel driftssituasjon.

Med kun én sjåfør har ikke lufthavnen lenger den samme operative "bufferen". Modellen velger å sende færre fly til remote-parkering fordi busskapasiteten er beslaglagt, noe som tvinger flere fly inn til terminalgatene. 


Det er viktig å understreke at denne simuleringen tar utgangspunkt i et deterministisk flyprogram. I den faktiske daglige driften forekommer forsinkelser av ulik grad – både ved ankomst og avgang – hver eneste dag. Når systemet allerede opererer "på grensen" med én sjåfør, vil slike uforutsette forskyvninger i flyprogrammet raskt kunne føre til at gate-konflikter forplanter seg og skaper betydelige køer som modellen i en ideell tilstand ikke fanger opp fullt ut. To sjåfører må derfor anses som et minimum for å opprettholde en robust drift som tåler daglige avvik.

**Scenario 2: Fremtidig trafikkvekst (+20 % i Peak)**
Dette scenariet simulerer en fremtidig situasjon hvor antall flybevegelser i den mest kritiske rushtiden (kl. 15:00–17:30) øker med 20 %. Hensikten var å undersøke om dagens gate-konfigurasjon og ressursallokering har tilstrekkelig reservekapasitet.

*Resultater:*

*   **Totalt antall fly håndtert:** 146 (en økning på 5 bevegelser i peak-vinduet).
*   **Gjennomsnittlig ventetid:** 0,96 minutter.
*   **Maksimal ventetid:** 15 minutter.
*   **Fly til Remote:** Økte til 13 fly.

*Analyse av kapasitetsreserve:*
Simuleringen viser at dagens infrastruktur ved Bergen Lufthavn har en betydelig innebygd robusthet. Ved å øke trafikken med 20 % i rushtiden, øker den gjennomsnittlige ventetiden kun marginalt fra 0,7 til 0,9 minutter. Dette skyldes i stor grad systemets evne til å distribuere mindre fly til remote-stands, noe som skjermer terminalkapasiteten for de største flyvningene.

Suksessfaktorene for å håndtere denne veksten er:

1.  **Aktiv gate-styring:** Den strategiske prioriteringen av store fly til gate-broer fungerer som en effektiv regulator.
2.  **Fleksibilitet i gate-oppsettet:** Utnyttelsen av flex-gater gjør det mulig å absorbere svingninger i trafikksammensetningen (D/I/S).
3.  **Tilstrekkelig busskapasitet:** To sjåfører er nok til å håndtere de ekstra remote-operasjonene uten at busskøer blir den begrensende faktoren.

Konklusjonen fra dette scenariet er at lufthavnen har kapasitet til moderat vekst med dagens operasjonsmodell, men at dette forutsetter at man opprettholder både personellressursene og den aktive styringen av parkeringsvalg. En ytterligere vekst utover 20 % vil sannsynligvis kreve enten fysiske utvidelser av terminalen eller mer radikale endringer i turnaround-prosesser.

### 4.4 Robusthet, følsomhet og anbefalte tilleggstester
Den nåværende simuleringsmodellen baserer seg på et fastlagt flyprogram uten tilfeldige stokastiske forsinkelser. Resultatene fra hver kjøring er derfor deterministiske. Dette gir god kontroll over årsakssammenhenger, men begrenser den statistiske generaliserbarheten. Funnene bør derfor tolkes som en analyse av strukturell kapasitet, ikke som en full sannsynlighetsanalyse av alle mulige driftsdager.

**1. Representativitet gjennom stress-testing**
Ved å velge 17. juni 2026 som utgangspunkt, analyseres en travel sommerdag i det planlagte flyprogrammet. I kapasitetsplanlegging er det ofte viktigere å forstå systemets oppførsel under høy belastning enn under gjennomsnittlig belastning. Resultatene gir derfor nyttig innsikt i hvordan systemet fungerer under press, men de gir ikke alene grunnlag for å konkludere om hele året.

**2. Følsomhet for bemanning**
Scenarioet med én busssjåfør viser at gjennomsnittlig ventetid bare øker marginalt, men at antall strategiske remote-parkeringer reduseres. Dette er et viktig funn fordi det viser at gjennomsnittlig ventetid alene ikke fanger opp systemets operative robusthet. Et system kan ha lav gjennomsnittlig ventetid, men likevel være sårbart dersom det mister fleksibiliteten til å flytte fly fra gate til remote stand.

**3. Behov for terskel- og persentilmål**
For å vurdere om systemet er robust bør analysen suppleres med indikatorer som 95-persentil for ventetid og andel fly som overstiger et definert terskelnivå:

$$
P(W_q > W_{max}) = \frac{\sum_{i=1}^{n} I(W_{q,i} > W_{max})}{n}
$$

der $I(W_{q,i} > W_{max})$ er lik 1 dersom fly $i$ venter mer enn terskelverdien, og 0 ellers. Dette målet er særlig relevant for operativ planlegging, fordi få ekstreme ventetider kan være viktigere enn et lavt gjennomsnitt.

**4. Foreslåtte tilleggstester**
For å styrke rapporten ytterligere bør modellen kjøres med følgende tilleggsscenarioer dersom tid og data tillater det:

| Tilleggstest | Forventet faglig bidrag |
|---|---|
| 0, 1, 2 og 3 busssjåfører | Identifiserer minimumsnivå og eventuell nytte av ekstra bemanning |
| Remote-strategi av/på | Viser om strategisk fjernparkering faktisk reduserer gatekonflikter |
| +10 %, +20 % og +30 % trafikkvekst | Identifiserer knekkpunktet for systemet |
| Tilfeldige ankomstforsinkelser | Tester om konklusjonene holder under mer realistisk drift |
| Økt busstid eller lavere busskapasitet | Tester hvor følsom modellen er for transportforutsetninger |

Disse testene vil gjøre det mulig å skille mellom tre ulike typer konklusjoner: hva systemet håndterer under ideelle forhold, hva systemet håndterer under realistisk variasjon, og hvilke ressurser som først blir kritiske når belastningen øker.

## 5. Diskusjon
### 5.1 Tolkning av funn
Simuleringsresultatene viser at dagens operasjonsmodell ved Bergen Lufthavn Flesland er svært effektiv under normale forhold. En gjennomsnittlig ventetid på under ett minutt for gate-tildeling på årets travleste dag indikerer et system i god balanse. Hovedårsaken til dette er ikke nødvendigvis et overskudd av gater, men den aktive styringen der mindre flyvninger (typisk Widerøe og regionale SAS-ruter) flyttes til remote-stands i peak-periodene.

Stresstesten i Scenario 1 avslørte imidlertid en skjult sårbarhet. Selv om ventetiden statistisk sett forble lav med kun én sjåfør, forsvant deler av systemets evne til å bruke fjernparkering som en strategisk "sikkerhetsventil". Dette tvinger flere fly inn til terminalen, noe som øker risikoen for kjedereaksjoner ved forsinkelser. Som påpekt i analysen, er virkeligheten preget av daglige avvik som ikke fanges opp i en deterministisk modell. Diskusjonen om bemanning bør derfor ikke bare handle om gjennomsnittlig tidsbruk, men også om risikoen for at systemet mister operativ fleksibilitet ved avvik.

Et viktig poeng er at lave gjennomsnittsverdier kan skjule sårbarhet i enkelthendelser. For en lufthavn kan én alvorlig gatekonflikt i peak-perioden være mer operativt krevende enn mange små ventetider fordelt utover dagen. Derfor bør maksimal ventetid, 95-persentil og andel fly over terskelverdi brukes sammen med gjennomsnittlig ventetid når resultatene tolkes.

### 5.2 Sammenligning med teori
Resultatene underbygger sentrale prinsipper i køteorien. Ved å flytte små fly til remote-stands, reduseres i praksis belastningen på de begrensede terminalgatene. I henhold til Littles Lov ($L = \lambda W$) vil lavere effektiv ankomstrate til en presset ressurs bidra til lavere gjennomsnittlig kø og ventetid, gitt at servicekapasiteten holdes stabil. I denne studien betyr det at remote stands fungerer som en avlastningsmekanisme for terminalgatene.

Samtidig viser resultatene hvorfor en enkel kømodell ikke er tilstrekkelig alene. Kapasiteten bestemmes ikke bare av antall gater, men av kombinasjonen av gatekompatibilitet, soneregler, turnaround-tider, remote stands, busser og busssjåfører. Den reelle kapasiteten er dermed et resultat av flere koblede ressurser.

Bruk av diskret-hendelse simulering (DES) har vist seg nødvendig for å fange opp samspillet mellom uavhengige ressurser. En ren analytisk modell ville hatt vanskeligheter med å illustrere hvordan mangelen på én sjåfør begrenser utnyttelsen av de fysiske parkeringsplassene på remote. Dette bekrefter at kapasitet ved en lufthavn ikke er en statisk verdi (antall gater), men en dynamisk funksjon av både infrastruktur, personell og logiske trafikkregler.

### 5.3 Praktiske implikasjoner
Basert på funnene i denne studien, trekkes følgende anbefalinger for Avinor:

1.  **Oppretthold bemanningsnivået:** To busssjåfører i rushtiden er kritisk, ikke for den gjennomsnittlige flyvningen, men for å opprettholde den operative fleksibiliteten som trengs for å håndtere daglige forsinkelser og unngå gate-konflikter ved terminalen.
2.  **Videreføring av strategisk fjernparkering:** Praksisen med å sende fly under 120 passasjerer til remote-stands i peak bør institusjonaliseres ytterligere, da simuleringen viser at dette er den viktigste faktoren for å absorbere trafikkvekst på inntil 20 %.
3.  **Digital tvilling for sanntidsstøtte:** Funnene viser at simulering er et kraftfullt verktøy for å evaluere kapasitet. Avinor bør vurdere å integrere lignende modeller i den daglige operative planleggingen (APOC) for å forutse gate-konflikter før de oppstår fysisk.

## 6. Konklusjon
### 6.1 Oppsummering
Denne studien har undersøkt effektiviteten av gate-utnyttelse og busstransport ved Bergen Lufthavn Flesland gjennom en diskret-hendelse simulering. Resultatene bekrefter at dagens operasjonsmodell, preget av strategisk bruk av fjernparkering for mindre flymaskiner i rushtiden, er svært robust og sikrer lave ventetider for passasjerene selv på de travleste dagene.

Hovedkonklusjonen er at dagens bemanningsnivå med to busssjåfører i rushtiden fungerer som en kritisk buffer for lufthavnens kapasitet. Simuleringen viser at lufthavnen kan håndtere en trafikkvekst på inntil 20 % med nåværende infrastruktur, forutsatt at man opprettholder den aktive styringen av flyparkering. Samtidig avslørte studien at en reduksjon i bemanning gjør systemet sårbart for kjedereaksjoner, noe som i en virkelig operasjon med daglige forsinkelser vil kunne føre til betydelige driftsproblemer.

### 6.2 Begrensninger ved studien
Selv om simuleringsmodellen gir verdifull innsikt, er det viktig å anerkjenne enkelte begrensninger:

*   **Deterministisk tilnærming:** Modellen baserer seg på et fastlagt ruteprogram uten stokastiske forsinkelser. I realiteten vil daglige avvik i ankomst- og avgangstider kunne forsterke kødannelser utover det modellen viser. Dette betyr at resultatene bør tolkes som strukturell kapasitetsanalyse, ikke som en full sannsynlighetsanalyse.
*   **Datakoblinger:** Bruken av historiske logger fra 2025 kombinert med et fremtidig ruteprogram for 2026 krever antagelser om flyrotasjoner som ikke nødvendigvis reflekterer selskapenes faktiske flåtestyring.
*   **Isolert system:** Studien har kun sett på gate- og busskapasitet. Faktorer som bagasjehåndtering, tilgang på bakkemannskap (ground handling) og værforhold er holdt utenfor modellen.

### 6.3 Forslag til videre forskning
For å videreutvikle forståelsen av kapasitetsutfordringene på Flesland, foreslås følgende områder for videre arbeid:

1.  **Stokastisk simulering:** Utvide modellen med Monte Carlo-metoder for å simulere tilfeldige forsinkelser, noe som vil gi et mer realistisk bilde av sårbarheten i Peak.
2.  **Integrert ressursmodellering:** Inkludere flere bakketjenester, som for eksempel tilgang på "pushback"-traktorer og bagasje-personell, for å identifisere kryssende flaskehalser.
3.  **Miljø- og kostnadsanalyse:** Utvide modellen til å beregne drivstofforbruk og utslipp knyttet til økt bruk av busser kontra tomgangskjøring ved gate-konflikter.

---

## Referanser
*   Avinor. (2025). Busslogger og operasjonelle data for Bergen Lufthavn Flesland.
*   Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). *Discrete-event system simulation*. Pearson.
*   Law, A. M. (2015). *Simulation modeling and analysis*. McGraw-Hill.
*   Pidd, M. (2004). *Computer Simulation in Management Science*. Wiley.
*   SimPy Documentation. (2024). *Discrete event simulation in Python*.

---

## Vedlegg
*A: Kildekode (Python/SimPy) - lokalisert i `src/simulation.py`*  
*B: Datavask-dokumentasjon - lokalisert i `src/clean_data.py`*
