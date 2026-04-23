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
### 4.3 Scenarieanalyse
For å besvare forskningsspørsmålene om systemets robusthet og kritiske grenser, ble det gjennomført to målrettede scenarieanalyser.

**Scenario 1: Redusert bemanning (Stress-test av sjåførkapasitet)**
I dette scenariet ble antall tilgjengelige busssjåfører redusert fra to til én på den travleste dagen i datasettet (17. juni). Hensikten var å identifisere hvor avhengig den strategiske gate-planleggingen er av kontinuerlig busskapasitet.

*Resultater:*
*   **Gjennomsnittlig ventetid:** Økte fra 0,7 til 0,9 minutter.
*   **Antall strategiske remote-parkeringer:** Redusert fra 11 til 8.
*   **Maksimal ventetid:** Vedvarte på 15 minutter.

*Analyse av sårbarhet:*
Selv om den gjennomsnittlige ventetiden kun økte marginalt i en ideell simulering, viser resultatene en betydelig økt sårbarhet i systemet. Med kun én sjåfør har ikke lufthavnen lenger den samme operative "bufferen". Modellen velger å sende færre fly til remote-parkering fordi busskapasiteten er beslaglagt, noe som tvinger flere fly inn til terminalgatene. 

Det er viktig å understreke at denne simuleringen tar utgangspunkt i et deterministisk flyprogram. I den faktiske daglige driften forekommer forsinkelser av ulik grad – både ved ankomst og avgang – hver eneste dag. Når systemet allerede opererer "på grensen" med én sjåfør, vil slike uforutsette forskyvninger i flyprogrammet raskt kunne føre til at gate-konflikter forplanter seg og skaper betydelige køer som modellen i en ideell tilstand ikke fanger opp fullt ut. To sjåfører må derfor anses som et minimum for å opprettholde en robust drift som tåler daglige avvik.

**Scenario 2: Fremtidig trafikkvekst (+20 % i Peak)**
Dette scenariet simulerer en fremtidig situasjon hvor antall flybevegelser i den mest kritiske rushtiden (kl. 15:00–17:30) øker med 20 %. Hensikten var å undersøke om dagens gate-konfigurasjon og ressursallokering har tilstrekkelig reservekapasitet.

*Resultater:*
*   **Totalt antall fly håndtert:** 147 (en økning på 6 bevegelser i peak-vinduet).
*   **Gjennomsnittlig ventetid:** 0,9 minutter.
*   **Maksimal ventetid:** 15 minutter.
*   **Fly til Remote:** Økte til 12 fly.

*Analyse av kapasitetsreserve:*
Simuleringen viser at dagens infrastruktur ved Bergen Lufthavn har en betydelig innebygd robusthet. Ved å øke trafikken med 20 % i rushtiden, øker den gjennomsnittlige ventetiden kun marginalt fra 0,7 til 0,9 minutter. Dette skyldes i stor grad systemets evne til å distribuere mindre fly til remote-stands, noe som skjermer terminalkapasiteten for de største flyvningene.

Suksessfaktorene for å håndtere denne veksten er:
1.  **Aktiv gate-styring:** Den strategiske prioriteringen av store fly til gate-broer fungerer som en effektiv regulator.
2.  **Fleksibilitet i gate-oppsettet:** Utnyttelsen av flex-gater gjør det mulig å absorbere svingninger i trafikk sammensetningen (D/I/S).
3.  **Tilstrekkelig busskapasitet:** To sjåfører er nok til å håndtere de ekstra remote-operasjonene uten at busskøer blir den begrensende faktoren.

Konklusjonen fra dette scenariet er at lufthavnen har kapasitet til moderat vekst med dagens operasjonsmodell, men at dette forutsetter at man opprettholder både personellressursene og den aktive styringen av parkeringsvalg. En ytterligere vekst utover 20 % vil sannsynligvis kreve enten fysiske utvidelser av terminalen eller mer radikale endringer i turnaround-prosesser.

### 4.4 Statistisk signifikans
*Analyse av variasjon i resultatene over flere iterasjoner.*

## 5. Diskusjon
### 5.1 Tolkning av funn
Simuleringsresultatene viser at dagens operasjonsmodell ved Bergen Lufthavn Flesland er svært effektiv under normale forhold. En gjennomsnittlig ventetid på under ett minutt for gate-tildeling på årets travleste dag indikerer et system i god balanse. Hovedårsaken til dette er ikke nødvendigvis et overskudd av gater, men den aktive styringen der mindre flyvninger (typisk Widerøe og regionale SAS-ruter) flyttes til remote-stands i peak-periodene.

Stresstesten i Scenario 1 avslørte imidlertid en skjult sårbarhet. Selv om ventetiden statistisk sett forble lav med kun én sjåfør, forsvant systemets evne til å bruke fjernparkering som en strategisk "sikkerhetsventil". Dette tvinger flere fly inn til terminalen, noe som øker risikoen for kjedereaksjoner ved forsinkelser. Som påpekt i analysen, er virkeligheten preget av daglige avvik som ikke fanges opp i en deterministisk modell. Diskusjonen om bemanning bør derfor ikke handle om gjennomsnittlig tidsbruk, men om risikoen for systemkollaps ved avvik.

### 5.2 Sammenligning med teori
Resultatene underbygger sentrale prinsipper i køteorien. Ved å flytte små fly til remote-stands, reduserer vi i praksis ankomstraten ($\lambda$) til de begrensede terminalgatene. I henhold til Littles Lov ($L = \lambda W$) fører dette direkte til lavere ventetid ($W$) for de store maskinene som er helt avhengige av gate-broer.

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
*   **Deterministisk tilnærming:** Modellen baserer seg på et fastlagt ruteprogram uten stokastiske forsinkelser. I realiteten vil daglige avvik i ankomst- og avgangstider kunne forsterke kødannelser utover det modellen viser.
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
*   Pidd, M. (2004). *Computer Simulation in Management Science*. Wiley.
*   SimPy Documentation. (2024). *Discrete event simulation in Python*.

---

## Vedlegg
*A: Kildekode (Python/SimPy) - lokalisert i `src/simulation.py`*  
*B: Datavask-dokumentasjon - lokalisert i `src/clean_data.py`*
