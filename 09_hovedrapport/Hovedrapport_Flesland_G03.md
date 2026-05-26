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
Bergen lufthavn Flesland er et sentralt knutepunkt for luftfarten på Vestlandet. I perioder med mange samtidige ankomster kan tilgjengelige terminalgater, remote stands, busser og busssjåfører bli begrensende ressurser. Når et ankommende fly ikke kan tildeles en egnet gate med en gang, kan det oppstå ventetid før parkering. Dersom flyet i stedet sendes til remote stand, krever dette samtidig tilgang på remote-plass, buss og sjåfør. Kapasitetsutfordringen handler derfor ikke bare om antall gater, men om samspillet mellom flere operative ressurser.

Utgangspunktet for denne rapporten er et datagrunnlag fra Avinor knyttet til flyprogram, rotasjoner og busslogger. Rapporten analyserer hvordan eksisterende ressurser kan utnyttes i peak-perioder uten å forutsette ny fysisk infrastruktur. Dette gjør problemstillingen relevant som beslutningsstøtte for operativ planlegging, særlig ved vurdering av gatebruk, strategisk fjernparkering og dimensjonering av busssjåførkapasitet.

Studien bruker diskret-hendelse simulering (DES) i Python med SimPy. Simulering er valgt fordi systemet består av hendelser som skjer på bestemte tidspunkter, for eksempel ankomst, gate-tildeling, frigjøring av gate og oppstart av busstransport. Metoden gjør det mulig å teste hvordan endringer i ressursnivå eller trafikkbelastning påvirker ventetid og ressursutnyttelse uten å eksperimentere i faktisk drift.

Rapporten er videre strukturert slik: Kapittel 2 presenterer det faglige og metodiske grunnlaget for analysen. Kapittel 3 beskriver forskningsdesign, datagrunnlag, modell og validering. Kapittel 4 presenterer resultater og scenarioanalyser. Kapittel 5 diskuterer funnene opp mot forskningsspørsmålene, mens kapittel 6 oppsummerer konklusjoner, begrensninger og forslag til videre arbeid.

### 1.2 Problemstilling
Hvilken effekt har endringer i flyprogram eller ressursallokering (busser, sjåfører og gater) på gateutnyttelse, bruk av fjernparkering og ventetider ved Bergen lufthavn Flesland?

Problemstillingen konkretiseres ved å analysere hvor mange ankomster systemet kan håndtere i et definert peak-vindu før kø, ventetid eller ressursutnyttelse indikerer at kapasiteten er presset. Studien vurderer særlig hvordan strategisk bruk av remote stands og dimensjonering av busssjåførkapasitet påvirker ventetid, gateutnyttelse og operativ robusthet.

### 1.3 Forskningsspørsmål
Studien tar sikte på å besvare følgende spørsmål gjennom simulering:
1. I hvilken grad bidrar dagens praksis med strategisk fjernparkering av mindre fly til å redusere gate-konflikter og ventetider i peak-perioder?
2. Hva er den kritiske grensen for antall busssjåfører før ventetiden for passasjerer øker markant i rushtiden?
3. Hvordan påvirkes ventetid, remote-bruk og gateutnyttelse av økt trafikk i peak-perioden?
4. Hvilke ressurser fremstår som de mest kritiske flaskehalsene: terminalgater, remote stands, busser eller busssjåfører?

### 1.4 Avgrensning
For å sikre en fokusert analyse av gate- og busskapasitet, er følgende faktorer holdt utenfor studiens omfang:

*   **Bagasjehåndtering:** Studien ser kun på flyets bevegelse og passasjertransport mellom fly og terminal. Flaskehalser i bagasjesystemet eller tilgang på bagasjevogner er ikke modellert.
*   **Teknisk pålitelighet og vedlikehold:** Modellen forutsetter 100 % oppetid på fysisk infrastruktur (broer, busser) og ser bort fra uforutsette tekniske feil eller vedlikeholdsstans i simuleringsperioden.
*   **Fysisk trafikkavvikling på taksebaner:** Kjøretider for busser er basert på gjennomsnittstall fra tilgjengelig datagrunnlag og inkluderer ikke sanntidsinteraksjon med flytrafikk eller andre kjøretøy på flyplassområdet som kan skape lokale forsinkelser.
*   **Ground handling:** Det forutsettes at eksterne tjenester som catering, drivstoff og teknisk vedlikehold utføres innenfor flyets planlagte turnaround-tid. Tilgang på personell fra handling-agenter er antatt å være ubegrenset.
*   **Værforhold:** Simuleringen tar utgangspunkt i normale operative forhold. Ekstremvær, avising eller snørydding er ikke inkludert.
*   **Sikkerhetskontroll og landside-kapasitet:** Studien fokuserer på airside-operasjoner. Kapasitetsutfordringer i terminalens avgangshall, sikkerhetskontroll eller passkontroll er ikke en del av modellen.

## 2. Faglig og metodisk grunnlag
### 2.1 Kildegrunnlag og avgrensning av teori
Denne rapporten bygger hovedsakelig på tre typer grunnlag: interne datasett fra Avinor, egen simuleringsmodell og metodisk støtte fra kompendiene i LOG650. Rammeverket for kvantitativ modellering, metodevalg og analyse er hentet fra *Kvantitative metoder i logistikk – implementert via KI* (Pettersen & Rekdal, 2026), mens struktur, kildebruk og akademisk fremstilling er støttet av *Vitenskapelig skriving – en praktisk innføring* (Rekdal & Pettersen, 2025). Det er ikke gjennomført en full systematisk litteraturgjennomgang av tidligere forskning på lufthavnsimulering eller gate-allokering. Rapportens teoretiske rammeverk må derfor forstås som et faglig og metodisk grunnlag for modellen, ikke som en uttømmende gjennomgang av forskningsfeltet.

Denne avgrensningen har betydning for hvordan funnene kan tolkes. Studien kan gi praksisnær innsikt i det konkrete systemet ved Bergen lufthavn Flesland, men den gir i mindre grad et teoretisk bidrag til forskningslitteraturen om lufthavnkapasitet. For å styrke rapporten ytterligere kunne en senere versjon sammenlignet modellen med tidligere forskning på gate-allokering, remote stand-bruk og diskret-hendelse simulering i lufthavndrift.

### 2.2 Køteori og kapasitetsplanlegging
Køteori er relevant fordi ankommende fly kan betraktes som en strøm av enheter som skal tildeles begrensede ressurser. I denne studien er de viktigste ressursene terminalgater, remote stands, busser og busssjåfører. Dersom en egnet ressurs ikke er tilgjengelig når et fly ankommer, oppstår ventetid.

Sentrale begreper i modellen er:
*   **Ankomstprosess:** tidspunktet fly ankommer systemet.
*   **Tjenestetid:** tiden et fly opptar en gate eller remote stand.
*   **Kødisiplin:** reglene som avgjør hvilket fly som får tilgang til en ressurs først.
*   **Ressursutnyttelse:** hvor stor andel av tilgjengelig kapasitet som faktisk er i bruk.

I en enkel kømodell kan sammenhengen mellom ankomster, antall enheter i systemet og ventetid beskrives med Littles lov, $L = \lambda W$. I denne rapporten brukes ikke formelen som en selvstendig beregningsmodell, men som et faglig begrep for å forstå hvorfor høyere belastning på en begrenset ressurs kan gi økt ventetid.

### 2.3 Diskret-hendelse simulering
Diskret-hendelse simulering (DES) er valgt fordi flyplassdrift består av hendelser som skjer på bestemte tidspunkter. Eksempler på slike hendelser er at et fly ankommer, en gate blir ledig, et fly sendes til remote stand eller en buss starter transport mellom stand og terminal.

DES er særlig egnet i denne studien fordi ressursene er gjensidig avhengige. Et fly som sendes til remote stand trenger ikke bare en ledig remote-plass, men også buss og sjåfør. Dersom én av disse ressursene mangler, kan systemet likevel få kø selv om de andre ressursene er ledige. Denne typen samspill er vanskelig å fange godt med en enkel statisk kapasitetsberegning.

### 2.4 Relevans for problemstillingen
Problemstillingen handler om hvordan endringer i flyprogram eller ressursallokering påvirker gateutnyttelse, remote-bruk og ventetider. Det faglige grunnlaget er derfor knyttet til tre forhold:

1. **Kapasitetsgrenser:** hvor mange samtidige ankomster systemet kan håndtere før ventetid oppstår.
2. **Ressurssamspill:** hvordan terminalgater, remote stands, busser og sjåfører påvirker hverandre.
3. **Robusthet:** hvordan systemet tåler endringer i trafikkbelastning eller bemanning.

Rapportens bidrag ligger først og fremst i å utvikle en praksisnær simuleringsmodell som kobler disse ressursene i ett samlet rammeverk. Dette gjør det mulig å analysere om ventetid skyldes mangel på gater, mangel på remote-kapasitet, mangel på busser eller mangel på sjåfører.

## 3. Metode
### 3.1 Forskningsdesign
Studien benytter et kvantitativt forskningsdesign basert på datasimulering. Dette designet er valgt fordi flyplassdrift er et "high-stakes" miljø hvor eksperimentering i reell drift er praktisk umulig, ekstremt kostbart og potensielt risikabelt for sikkerheten og punktligheten.

Simulering som forskningsmetode gir oss et "digitalt laboratorium" hvor vi kan:

1.  **Isolere variabler:** Vi kan endre nøyaktig én variabel (f.eks. antall busssjåfører) mens vi holder flyprogrammet og gatestrukturen helt konstant, noe som gjør det mulig å identifisere direkte årsakssammenhenger.
2.  **Stress-teste systemet:** Vi kan simulere ekstreme scenarioer, som 20% trafikkvekst, for å identifisere "knekkpunkter" i infrastrukturen før de oppstår i virkeligheten.
3.  **Dokumentere "As-Is" vs. "To-Be":** Ved først å verifisere en baseline-modell mot dagens drift, skapes et solid fundament for å evaluere effekten av fremtidige strategiske endringer.

### 3.2 Datainnsamling og Datapreparering
Datagrunnlaget for studien består av tre hovedkilder levert av Avinor (Avinor, 2025, 2026):

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

### 3.5 Verifisering og validering
For å vurdere modellens pålitelighet er det skilt mellom verifisering og validering. Verifisering handler om hvorvidt modellen er programmert i tråd med den logikken som er beskrevet, mens validering handler om hvorvidt modellen gir et rimelig bilde av den operative situasjonen som analyseres.

**Verifisering (bygge modellen riktig):**
Verifiseringen har fokusert på å kontrollere at den programmerte logikken i SimPy samsvarer med de tiltenkte reglene for lufthavndriften:
*   **Trace-logger:** Det er brukt hendelseslogger under utviklingen for å kontrollere at fly sendes til riktige soner og at flex-gate-restriksjoner overholdes.
*   **Stresstesting av logikk:** Koden er testet med ekstreme verdier, for eksempel null sjåfører, for å undersøke om kømekanismer og ressursbegrensninger oppfører seg som forventet.
*   **Kontroll av enkeltfunksjoner:** Funksjoner som `sjekk_sone_konflikt` og `finn_ledig_gate` er kontrollert isolert for å se om de gir forventede utfall i ulike parkeringsscenarioer.

**Validering (bygge den riktige modellen):**
Full kvantitativ validering mot historiske observasjoner har ikke vært mulig innenfor prosjektets rammer, fordi datagrunnlaget ikke inneholder direkte sammenlignbare mål for alle simulerte variabler. Særlig gjelder dette historisk ventetid før gate, faktisk remote-bruk i samme struktur som modellen og direkte sammenlignbare scenarioer for ulike sjåførnivåer. Valideringen er derfor gjennomført som en kombinasjon av face validity, kalibrering av enkelte tidsparametere og plausibilitetssjekk av baseline-scenarioet.

| Valideringsform | Hva som er kontrollert | Begrensning |
|---|---|---|
| Face validity | Om baseline-resultatene virker realistiske sammenlignet med forventet driftssituasjon | Bygger på faglig vurdering, ikke komplett historisk fasit |
| Kalibrering mot busslogger | Om tidsbruk for busstransport ligger på et rimelig nivå | Busslogger gir ikke nødvendigvis full sammenligning for alle scenarioer |
| Baseline-sjekk | Om modellen håndterer hele testdagen uten systemstans eller urimelige køtopper | Viser plausibilitet, men ikke statistisk treffsikkerhet |
| Stresstest | Om modellen reagerer logisk når sjåførkapasitet reduseres | Tester modellatferd, ikke nødvendigvis faktisk historisk drift |

Denne valideringsformen betyr at resultatene bør tolkes som et beslutningsstøttende analysegrunnlag, ikke som en eksakt prediksjon av faktiske ventetider. Modellen er best egnet til å sammenligne scenarioer og identifisere relative forskjeller mellom ressursoppsett, for eksempel forskjellen mellom én og to busssjåfører eller effekten av strategisk remote-bruk.

### 3.6 Gjennomførte og anbefalte scenarioer
For å styrke analysens etterprøvbarhet er scenarioene strukturert som kontrollerte eksperimenter der én sentral parameter endres om gangen. Noen av scenarioene er gjennomført i denne rapporten, mens andre beskrives som anbefalte tilleggstester dersom modellen videreutvikles.

| Test | Parameter som endres | Status | Formål |
|---|---|---|---|
| Baseline | Dagens ressursnivå | Gjennomført | Referansepunkt for sammenligning |
| Sjåførkapasitet | 0, 1, 2 og 3 sjåfører | Gjennomført | Finne kritisk bemanningsnivå |
| Trafikkvekst | +10 %, +20 % og +30 % i peak | Gjennomført | Identifisere kapasitetsgrense |
| Remote-strategi | Strategisk remote av/på | Gjennomført | Måle effekt av aktiv gate-styring |
| Busstid | +20 % kjøretid | Gjennomført | Teste følsomhet for transporttid |
| Busskapasitet | 60, 70, 80 og 90 passasjerer | Anbefalt tilleggstest | Teste effekt av kapasitet per buss |
| Stokastiske forsinkelser | Lav, middels og høy forsinkelsesvariasjon | Delvis gjennomført / anbefalt videreført | Teste robusthet under realistiske avvik |

Dersom stokastiske forsinkelser inkluderes fullt ut, bør hvert scenario kjøres mange ganger, for eksempel 100 eller 500 replikasjoner. Da kan resultatene presenteres med gjennomsnitt, standardavvik og 95 % konfidensintervall:

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

Tabell 1 oppsummerer de simulerte hovedresultatene fra scenarioene som hittil er gjennomført. I en videreutvikling av analysen kan tabellen utvides med 95-persentil, gateutnyttelse og sjåførutnyttelse dersom disse målene hentes ut fra simuleringsmodellen.

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

Verdien 15 minutter går igjen som maksimal ventetid i flere scenarioer. Dette bør tolkes med varsomhet. Når samme maksimumsverdi opptrer gjentatte ganger, kan det tyde på at verdien delvis følger av modellens tidslogikk, for eksempel diskretisering, ventesteg eller en bestemt operasjonell terskel i simuleringen, og ikke nødvendigvis er et tilfeldig observert maksimum. Verdien er likevel nyttig som indikator på at enkelte fly møter en kapasitetskonflikt, men den bør ikke tolkes som en presis prediksjon av faktisk maksimal ventetid uten nærmere kontroll av trace-loggene.


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
### 5.1 FS1: Effekt av strategisk fjernparkering
Det første forskningsspørsmålet handler om i hvilken grad strategisk fjernparkering av mindre fly bidrar til å redusere gatekonflikter og ventetider i peak-perioder. Resultatene tyder på at strategisk remote-bruk har en positiv effekt. I baseline-scenarioet håndteres 141 fly, hvor 130 parkeres ved gate og 11 sendes til remote. Gjennomsnittlig ventetid er 0,71 minutter. Når remote-strategien slås av, øker gjennomsnittlig ventetid til 1,21 minutter, samtidig som flere fly presses inn mot terminalgatene.

Dette indikerer at remote stands fungerer som en avlastningsmekanisme for terminalgatene. Effekten er ikke først og fremst at alle fly får kortere ventetid, men at systemet får større fleksibilitet til å prioritere store fly og fly med høyere behov for terminalnær parkering. Strategisk fjernparkering bør derfor forstås som et virkemiddel for robusthet, ikke bare som en løsning for enkelttilfeller med manglende gatekapasitet.

### 5.2 FS2: Kritisk grense for busssjåfører
Det andre forskningsspørsmålet gjelder hvor grensen går for antall busssjåfører før ventetiden øker markant. Scenarioene viser at to sjåfører fremstår som et hensiktsmessig minimum i peak-perioden. Med én sjåfør øker gjennomsnittlig ventetid fra 0,71 til 0,92 minutter, og antall remote-operasjoner reduseres fra 11 til 8. Dette er ikke en dramatisk økning i gjennomsnittlig ventetid, men det viser at systemet mister noe av fleksibiliteten til å bruke remote stands aktivt.

Scenarioet med null sjåfører viser tydeligere hvor viktig sjåførressursen er. Da øker gjennomsnittlig ventetid til 2,16 minutter, og maksimal ventetid blir 60 minutter. Dette viser at busssjåfører er en kritisk ressurs, ikke bare fordi de transporterer passasjerer, men fordi de gjør remote stands operativt tilgjengelige. Uten sjåfører eksisterer remote-kapasiteten i praksis bare som fysisk areal, ikke som en fullt brukbar kapasitetsressurs.

Resultatene viser også at tre sjåfører ikke gir lavere gjennomsnittlig ventetid enn to sjåfører i baseline-lignende drift. Det tyder på at to sjåfører er nok i den analyserte situasjonen, mens tre sjåfører først kan bli relevant ved større forsinkelser, høyere trafikkvekst eller lengre busstider.

### 5.3 FS3: Effekt av trafikkvekst i peak-perioden
Det tredje forskningsspørsmålet undersøker hvordan økt trafikk påvirker ventetid, remote-bruk og gateutnyttelse. I scenarioet med 20 % trafikkvekst i peak øker det totale antallet fly i simuleringen fra 141 til 146, altså fem ekstra flybevegelser. Gjennomsnittlig ventetid øker fra 0,71 til 0,96 minutter, og antall remote-operasjoner øker fra 11 til 13.

Resultatene tyder på at dagens operasjonsmodell tåler moderat trafikkvekst, forutsatt at strategisk remote-bruk og to sjåfører opprettholdes. Samtidig bør prosentvis vekst tolkes sammen med faktisk antall ekstra fly. En økning på 20 % i peak-vinduet gir i denne simuleringen bare fem ekstra fly totalt i den analyserte dagen. Det betyr at scenarioet viser robusthet mot moderat økning, men ikke nødvendigvis mot en vesentlig endret trafikkstruktur eller flere samtidige store fly.

### 5.4 FS4: Kritiske flaskehalser
Det fjerde forskningsspørsmålet handler om hvilke ressurser som fremstår som mest kritiske: terminalgater, remote stands, busser eller busssjåfører. Resultatene peker ikke på én enkelt fysisk ressurs som alene bestemmer kapasiteten. Flaskehalsen oppstår snarere i samspillet mellom gatekapasitet og busssjåførkapasitet.

Terminalgatene er sentrale fordi store fly og visse trafikktyper har sterkere behov for terminalnær parkering. Remote stands gir fleksibilitet, men bare dersom busser og sjåfører er tilgjengelige. Busssjåfører fremstår derfor som en særlig kritisk koblingsressurs: De avgjør om remote stands faktisk kan brukes som avlastning for gatekapasiteten.

Dette betyr at kapasitetsplanleggingen ikke bør begrenses til å telle antall gater eller antall remote stands. Den bør også inkludere hvordan ressursene virker sammen over tid. En lufthavn kan ha tilstrekkelig fysisk kapasitet, men likevel få kø dersom personellressurser eller transportressurser ikke er tilgjengelige på riktig tidspunkt.

### 5.5 Samlet vurdering og praktiske implikasjoner
Samlet viser analysen at dagens operasjonsmodell ved Bergen lufthavn Flesland er robust i den analyserte testdagen, men at robustheten er avhengig av aktiv styring. Lave gjennomsnittsverdier for ventetid kan skjule sårbarhet i enkelthendelser. For en lufthavn kan én alvorlig gatekonflikt i peak-perioden være mer operativt krevende enn mange små ventetider fordelt utover dagen. Derfor bør maksimal ventetid, 95-persentil og andel fly over terskelverdi brukes sammen med gjennomsnittlig ventetid når resultatene tolkes.

Basert på funnene trekkes tre praktiske anbefalinger:

1. **Oppretthold minst to busssjåfører i peak-perioder.** To sjåfører ser ut til å gi nødvendig operativ fleksibilitet, mens én sjåfør gjør systemet mer sårbart.
2. **Viderefør strategisk fjernparkering av mindre fly.** Dette frigjør terminalnære gater til større eller mer kapasitetskrevende fly.
3. **Bruk simulering som beslutningsstøtte.** En videreutviklet modell kan brukes til å teste trafikkvekst, forsinkelser og bemanningsendringer før tiltak innføres i faktisk drift.

Rapportens metodiske bidrag er at den viser hvordan koblede ressurser, gate, remote stand, buss og sjåfør, kan modelleres i ett samlet DES-rammeverk. Dette gir et mer realistisk bilde av operativ kapasitet enn en statisk vurdering av antall tilgjengelige gater alene.

## 6. Konklusjon
### 6.1 Svar på forskningsspørsmålene
Denne studien har undersøkt hvordan endringer i flyprogram og ressursallokering påvirker gateutnyttelse, bruk av fjernparkering og ventetider ved Bergen lufthavn Flesland. Analysen er gjennomført som en diskret-hendelse simulering basert på tilgjengelige datasett og en modell som kobler terminalgater, remote stands, busser og busssjåfører.

Studien gir følgende svar på forskningsspørsmålene:

*   **FS1 – Strategisk fjernparkering:** Strategisk fjernparkering av mindre fly bidrar til å redusere presset på terminalgatene og gir systemet større fleksibilitet i peak-perioder. Når remote-strategien slås av, øker gjennomsnittlig ventetid, og flere fly må håndteres ved terminalgatene.
*   **FS2 – Kritisk sjåførnivå:** To busssjåfører fremstår som et hensiktsmessig minimum i den analyserte peak-perioden. Én sjåfør gir fortsatt lav gjennomsnittlig ventetid, men reduserer muligheten til å bruke remote stands aktivt. Null sjåfører gir tydelig kapasitetsbrudd og høy maksimal ventetid.
*   **FS3 – Trafikkvekst:** Systemet ser ut til å kunne håndtere moderat trafikkvekst i peak-perioden, blant annet en økning på 20 % i det analyserte peak-vinduet. Dette forutsetter at dagens ressursnivå og strategiske remote-bruk opprettholdes.
*   **FS4 – Flaskehalser:** Den viktigste flaskehalsen er ikke én enkelt ressurs, men samspillet mellom terminalgater, remote stands og busssjåførkapasitet. Busssjåfører fungerer som en koblingsressurs som avgjør om remote stands faktisk kan brukes som avlastning for terminalgatene.

Hovedkonklusjonen er at dagens operasjonsmodell virker robust for den analyserte testdagen, men at robustheten er avhengig av aktiv gate-styring og tilstrekkelig sjåførkapasitet. Modellen viser at fysisk infrastruktur alene ikke bestemmer kapasiteten. Operativ kapasitet oppstår gjennom samspillet mellom infrastruktur, transportressurser, bemanning og prioriteringsregler.

### 6.2 Studiens bidrag
Studiens praktiske bidrag er at den gir et beslutningsstøttende analysegrunnlag for planlegging av gatebruk, remote stands og busssjåførkapasitet ved Bergen lufthavn Flesland. Resultatene kan brukes til å vurdere hvilke ressursnivåer som bør opprettholdes i peak-perioder, og hvilke scenarioer som bør undersøkes nærmere før operative endringer innføres.

Studiens metodiske bidrag er at den viser hvordan diskret-hendelse simulering kan brukes til å modellere flere koblede bakkestøtteressurser i ett samlet rammeverk. Dette gjør det mulig å analysere kapasitetsutfordringer som ikke ville vært like synlige i en enkel statisk kapasitetsberegning.

### 6.3 Begrensninger ved studien
Selv om simuleringsmodellen gir verdifull innsikt, er det viktig å anerkjenne enkelte begrensninger:

*   **Begrenset litteraturgrunnlag:** Rapporten bygger primært på datagrunnlaget, egen modell og metodisk støtte fra LOG650-kompendiene. Det er ikke gjennomført en bred litteraturgjennomgang av tidligere forskning på lufthavnsimulering eller gate-allokering.
*   **Deterministisk hovedmodell:** Modellen baserer seg hovedsakelig på et fastlagt ruteprogram uten full stokastisk modellering av forsinkelser. I realiteten vil daglige avvik i ankomst- og avgangstider kunne forsterke køer utover det modellen viser.
*   **Begrenset kvantitativ validering:** Full sammenligning mellom historiske observasjoner og simulert baseline har ikke vært mulig for alle måleparametere. Resultatene bør derfor tolkes som scenarioanalyse og beslutningsstøtte, ikke som eksakte prediksjoner.
*   **Datakoblinger:** Bruken av historiske logger kombinert med et fremtidig ruteprogram krever antakelser om flyrotasjoner som ikke nødvendigvis reflekterer selskapenes faktiske flåtestyring.
*   **Isolert system:** Studien har kun sett på gate- og busskapasitet. Faktorer som bagasjehåndtering, tilgang på bakkemannskap og værforhold er holdt utenfor modellen.

### 6.4 Forslag til videre forskning
For å videreutvikle forståelsen av kapasitetsutfordringene på Flesland, foreslås følgende områder for videre arbeid:

1.  **Stokastisk simulering:** Utvide modellen med Monte Carlo-metoder for å simulere tilfeldige forsinkelser og beregne konfidensintervaller for ventetid og ressursutnyttelse.
2.  **Flere analysedager:** Kjøre modellen for flere travle dager, for eksempel alle peak-dager i juni, for å undersøke om funnene fra 17. juni er representative.
3.  **Utvidet ressursmodellering:** Inkludere flere bakketjenester, som pushback-traktorer, bagasjepersonell og handlingressurser, for å identifisere kryssende flaskehalser.
4.  **Kostnads- og miljøanalyse:** Utvide modellen til å beregne kostnader, overflødig bemanningstid og eventuelle miljøeffekter knyttet til ulike remote- og bussoppsett.

---

## Referanser
*   Avinor. (2025). *Busslogger og operasjonelle data for Bergen lufthavn Flesland* [Upublisert datasett].
*   Avinor. (2026). *Flyprogram og rotasjonsdata for Bergen lufthavn Flesland* [Upublisert datasett].
*   Pettersen, B.-I., & Rekdal, P. K. (2026). *Kvantitative metoder i logistikk – implementert via KI* [Kompendium]. Høgskolen i Molde.
*   Rekdal, P. K., & Pettersen, B.-I. (2025). *Vitenskapelig skriving – en praktisk innføring* [Kompendium]. Høgskolen i Molde.

---

## Vedlegg
*A: Kildekode (Python/SimPy) - lokalisert i `04_src/simulation.py`*  
*B: Datavask-dokumentasjon - lokalisert i `04_src/clean_data.py`*
