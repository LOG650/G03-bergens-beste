
# Kapasitetsanalyse for samtidige ankomster ved Bergen lufthavn Flesland
## Prosjektstyringsplan – LOG650

**Prosjektleder:** Sandra Christensen  
**Emne:** LOG650 – Høyskolen i Molde  
**Casebedrift:** Avinor – Bergen lufthavn Flesland  
**Innlevering:** 1. juni 2026  

---

# Innholdsfortegnelse

1. Sammendrag  
2. Behov  
3. Sponsor  
4. Kunde  
5. Forretningscase  
6. Gevinster  
7. Omfang  
8. Krav  
9. Løsning  
10. Arbeidsnedbrytningsstruktur (WBS)  
11. Fremdrift  
12. Milepæler  
13. Risikoanalyse  
14. Kommunikasjonsplan  
15. Endringskontroll  
16. Godkjenning  

---

# 1. Sammendrag

Dette dokumentet utgjør prosjektstyringsplanen for prosjektet *Kapasitetsanalyse for samtidige ankomster ved Bergen lufthavn Flesland*. Dokumentet beskriver prosjektets mål, omfang, fremdriftsplan, metode og risiko.

Prosjektet analyserer hvordan eksisterende ressurser ved Bergen lufthavn Flesland kan utnyttes mer effektivt i perioder med mange samtidige flyankomster.

Fokusområder:

- gater
- remote stands
- busser
- bussjåfører

Analysen baseres på:

- køteori
- kapasitetsplanlegging
- diskret hendelses-simulering (DES)

Resultatet skal gi et bedre beslutningsgrunnlag for planlegging av bussressurser og håndtering av samtidige ankomster uten behov for ny infrastruktur.

---

# 2. Behov

Bergen lufthavn Flesland opplever perioder med høy trafikkbelastning der flere fly ankommer samtidig.

Begrensninger i:

- gatekapasitet
- remote stands
- bussressurser
- tilgjengelige bussjåfører

kan føre til ventetid før fly får oppstillingsplass.

Dette kan skape:

- gate-relaterte forsinkelser
- ineffektiv ressursbruk
- økte operasjonelle kostnader

I tillegg planlegges innleie av bussjåfører ofte basert på forventet trafikk flere uker i forkant. Dersom trafikken blir lavere enn forventet kan dette føre til overflødige arbeidstimer.

Det er derfor behov for et analyseverktøy som kan:

- estimere hvor mange samtidige ankomster systemet kan håndtere
- analysere effekten av gatebruk og remote stands
- optimalisere bruk av bussressurser
- redusere ventetid før gate
- redusere overflødig kapasitet for innleide bussjåfører

---

# 3. Sponsor

Sponsor for prosjektet er **Høyskolen i Molde**, gjennom emnet **LOG650**.

Faglærer fungerer som:

- faglig veileder
- oppdragsgiver
- evaluator av prosjektet

---

# 4. Kunde

Kunden i prosjektet representerer den operative planleggingsfunksjonen ved:

**Avinor – Bergen lufthavn Flesland**

Resultatene kan potensielt brukes til:

- operativ planlegging
- gatekoordinering
- planlegging av bussressurser
- dimensjonering av innleide bussjåfører

---

# 5. Forretningscase

## Alternativer

### Alternativ 1 – Status quo
Dagens praksis videreføres uten analytisk modellering.

Konsekvens:
- begrenset innsikt i kapasitetsgrenser
- potensielt ineffektiv ressursbruk

### Alternativ 2 – Analyse og simulering (valgt)
Utvikle en simuleringsmodell for å analysere optimal bruk av eksisterende ressurser.

Fordeler:
- bedre beslutningsgrunnlag
- ingen investering i ny infrastruktur

### Alternativ 3 – Infrastrukturutvidelse
Bygge nye gater eller stands.

Ulemper:
- høy investeringskostnad
- utenfor prosjektets omfang

---

# 6. Gevinster

Forventede gevinster:

- bedre forståelse av kapasitetsgrenser
- redusert ventetid før gate
- bedre utnyttelse av gater og stands
- mer effektiv bruk av busser
- bedre planlegging av bussjåførressurser
- redusert overflødig kapasitet

---

# 7. Omfang

## Mål

Utvikle en analysemodell som kan estimere hvor mange samtidige ankomster Bergen lufthavn Flesland kan håndtere i peak-perioder uten at ventetid før gate overstiger et definert nivå.

## Avgrensninger

- ingen ny fysisk infrastruktur
- rutetider antas gitt
- fokus på ankomstfasen
- bemanning ved gater modelleres ikke eksplisitt
- buss og bussjåfører modelleres som begrensende ressurser
- analysen baseres på representative eller simulerte data

---

# 8. Krav

Prosjektet må:

- analysere samtidige ankomster
- inkludere gater og remote stands
- inkludere bussressurser
- inkludere bussjåfører
- estimere ventetid før gate
- analysere alternative scenarier
- estimere behov for bussjåfører

---

# 9. Løsning

Prosjektet utvikler en **diskret hendelses-simuleringsmodell**.

Modellen inkluderer:

- flyankomster
- gateallokering
- remote stands
- bussdistribusjon
- bussjåfører
- turnaround-tider

Simuleringen brukes til å analysere:

- kapasitet
- ventetid
- ressursutnyttelse

---

# 10. Arbeidsnedbrytningsstruktur (WBS)

## Prosjektoppstart
- definere problemstilling
- avklare omfang

## Datainnsamling
- identifisere datakilder
- strukturere trafikkdata

## Modellutvikling
- utvikle konseptuell modell
- implementere simuleringsmodell

## Analyse
- kjøre simuleringer
- analysere ventetid og kapasitet

## Scenarioanalyse
- teste alternative ressursoppsett

## Rapportering
- tolke resultater
- skrive rapport

---

# 11. Fremdrift

Prosjektperiode:

**Mars – 1. juni 2026**

Faser:

1. Problemdefinisjon  
2. Datainnsamling  
3. Modellutvikling  
4. Simulering  
5. Analyse  
6. Rapportskriving  

---

# 12. Milepæler

M1 – Godkjent prosjektbeskrivelse  
M2 – Datagrunnlag etablert  
M3 – Konseptuell modell ferdig  
M4 – Simuleringsmodell ferdig  
M5 – Scenarioanalyse gjennomført  
M6 – Rapportutkast ferdig  
M7 – Endelig innlevering  

---

# 13. Risikoanalyse

## Risiko 1 – Manglende data
Tiltak: bruke estimater og simulert data.

## Risiko 2 – For kompleks modell
Tiltak: fokusere på gater, stands, busser og bussjåfører.

## Risiko 3 – Tidsbegrensninger
Tiltak: tydelige milepæler.

## Risiko 4 – Validering
Tiltak: sensitivitetsanalyse.

---

# 14. Kommunikasjonsplan

Kommunikasjon skjer mellom:

- student
- faglærer / veileder

Kanaler:

- e-post
- veiledningsmøter
- rapportdokumentasjon

---

# 15. Endringskontroll

Eventuelle endringer i:

- datagrunnlag
- modellstruktur
- scenarier

skal dokumenteres og vurderes opp mot prosjektets mål.

---

# 16. Godkjenning

Prosjektleder:  
Sandra Christensen  

Prosjekt:  
Kapasitetsanalyse for samtidige ankomster ved Bergen lufthavn Flesland  

Innleveringsfrist:  
1. juni 2026
