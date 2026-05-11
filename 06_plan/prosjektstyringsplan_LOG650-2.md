# Kapasitetsanalyse for samtidige ankomster ved Bergen lufthavn Flesland
## Prosjektstyringsplan – LOG650

**Utarbeidet av:** Sandra Christensen (Prosjektleder)  
**Autorisert av:** Bård Inge Pettersen og Per Kristian Rekdal (Faglærere/Sponsorer)  
**Dato:** 9. mars 2026  
**Innleveringsfrist:** 1. juni 2026  

---

# Innholdsfortegnelse
1. [Sammendrag](#1-sammendrag)
2. [Behov](#2-behov)
3. [Sponsor](#3-sponsor)
4. [Kunde](#4-kunde)
5. [Forretningscase](#5-forretningscase)
6. [Omfang](#6-omfang)
7. [Fremdrift](#7-fremdrift)
8. [Risiko](#8-risiko)
9. [Saker](#9-saker)
10. [Interessenter](#10-interessenter)
11. [Ressurser](#11-ressurser)
12. [Kommunikasjon](#12-kommunikasjon)
13. [Kvalitet](#13-kvalitet)
14. [Anskaffelser](#14-anskaffelser)
15. [Endringskontrollprosess](#15-endringskontrollprosess)
16. [Vedlegg](#16-vedlegg)

---

# 1. Sammendrag
Dette dokumentet utgjør prosjektstyringsplanen for prosjektet *Kapasitetsanalyse for samtidige ankomster ved Bergen lufthavn Flesland*. Dokumentet dokumenterer planbaselines for omfang, fremdrift og risiko, og gir tilleggsinformasjon for å støtte prosjektleder i vellykket gjennomføring.

Prosjektet støtter følgende mål i LOG650 sin strategiske plan: «Anvendelse av kvantitative metoder og simulering for å løse logistiske utfordringer i praksis».

Dette er et levende dokument som oppdateres av prosjektleder ved behov gjennom prosjektets løpetid.

---

# 2. Behov
Bergen lufthavn Flesland opplever perioder med høy trafikkbelastning der flere fly ankommer samtidig. Behovet for prosjektet springer ut av en hypotese om at nåværende ressursbruk (busser og sjåfører) ved samtidige ankomster kan optimaliseres. Uten en analytisk modell er det utfordrende å forutse nøyaktig når kapasitetstaket nås, noe som kan føre til enten forsinkelser for passasjerer eller unødvendig høye kostnader ved beredskap.

Dette skaper behov for et analyseverktøy som kan:
- Estimere systemets kapasitet for samtidige ankomster.
- Optimalisere bruk av bussressurser.
- Redusere ventetid og overflødig kapasitet hos innleide sjåfører.

---

# 3. Sponsor
Sponsor for prosjektet er **Høyskolen i Molde**, gjennom emnet **LOG650**. Faglærerne **Bård Inge Pettersen** og **Per Kristian Rekdal** fungerer som faglige veiledere og myndighet for godkjenning av prosjektplanen og eventuelle endringer.

---

# 4. Kunde
Kunden representerer den operative planleggingsfunksjonen ved **Avinor – Bergen lufthavn Flesland**. Resultatene skal kunne brukes til operativ planlegging og dimensjonering av ressurser.

---

# 5. Forretningscase

### Alternativer
1. **Alternativ 1 – Status quo:** Dagens praksis videreføres. Forkastet fordi det gir begrenset innsikt i kapasitetsgrenser og risiko for ineffektiv ressursbruk.
2. **Alternativ 2 – Analyse og simulering (valgt):** Utvikle en simuleringsmodell. Valgt fordi det gir best beslutningsstøtte med lave kostnader (studentarbeid).
3. **Alternativ 3 – Infrastrukturutvidelse:** Bygge nye gater. Forkastet grunnet ekstremt høye investeringskostnader og tidsbruk.

### Forutsetninger
- **Tilgang til data:** Gjennomføring av valgt alternativ (simulering) er betinget av at Avinor leverer nødvendige historiske trafikkdata og operative logger innen utgangen av mars 2026.
- **Programvare:** Tilgang til nødvendig programvare for simulering (Python/SimPy).

### Gevinster
- Bedre forståelse av kapasitetsgrenser.
- Redusert ventetid før gate.
- Mer effektiv bruk av busser og personellressurser.

### Kostnader
Prosjektet gjennomføres som et studentprosjekt. Kostnadene består primært av medgått tid.

### Analyse
Sammenligningen viser at Alternativ 2 gir høyest verdi gjennom innsikt uten behov for fysiske investeringer.

---

# 6. Omfang

### Mål
Utvikle en analysemodell som kan estimere hvor mange samtidige ankomster Bergen lufthavn Flesland kan håndtere i peak-perioder uten at ventetid før gate overstiger et definert nivå.

### Krav
- Analysere samtidige ankomster inkludert gater og remote stands.
- Modellere bussressurser og bussjåfører som begrensende faktorer.
- Estimere ventetid og ressursutnyttelse.

### Løsning
Prosjektet utvikler en **diskret hendelses-simuleringsmodell (DES)** i Python som inkluderer flyankomster, gateallokering, busstransport og turnaround-tider.

### Arbeidsnedbrytningsstruktur (WBS)
- [x] **1. Prosjektoppstart:** Definere problemstilling og rammer.
- [x] **2. Datainnsamling:** Strukturere trafikkdata fra Avinor.
- [ ] **3. Modellutvikling:** Utvikle konseptuell og teknisk simuleringsmodell.
- [ ] **4. Analyse:** Kjøre simuleringer og scenarioanalyser.
- [ ] **5. Rapportering:** Tolke resultater og skrive endelig rapport.

---

# 7. Fremdrift

### Gantt-diagram (Prosjektfremdrift)
```mermaid
gantt
    title Prosjektfremdrift: Kapasitetsanalyse Flesland (LOG650)
    dateFormat  YYYY-MM-DD
    section Planlegging
    Prosjektoppstart & Plan :done, p1, 2026-02-15, 2026-03-09
    Milepæl M1: Godkjent beskrivelse :milestone, m1, 2026-03-09, 0d

    section Datainnsamling
    Innhenting av trafikkdata (Avinor) :done, p2, 2026-03-09, 2026-03-31
    Strukturering av datagrunnlag :done, p3, 2026-03-20, 2026-04-07
    Milepæl M2: Datagrunnlag etablert :milestone, m2, 2026-04-07, 0d

    section Utvikling
    Konseptuell modellering :active, p4, 2026-04-01, 2026-04-30
    Milepæl M3: Konseptuell modell ferdig :milestone, m3, 2026-04-30, 0d
    Programmering (Python/SimPy) :p5, 2026-05-01, 2026-05-15
    Milepæl M4: Simuleringsmodell ferdig :milestone, m4, 2026-05-15, 0d

    section Analyse & Rapport
    Baseline-analyse & Testing :p6, 2026-05-16, 2026-05-22
    Scenarioanalyse :p7, 2026-05-20, 2026-05-26
    Sluttføring av rapport :p8, 2026-05-20, 2026-05-31
    Innlevering :crit, p9, 2026-06-01, 1d
    Milepæl M5: Endelig innlevering :milestone, m5, 2026-06-01, 0d
```

### Milepæler
- [x] **M1:** Godkjent prosjektbeskrivelse (Ferdigstilt 09.03.26)
- [x] **M2:** Datagrunnlag etablert (Ferdigstilt 07.04.26)
- [ ] **M3:** Konseptuell modell ferdig (Planlagt April)
- [ ] **M4:** Simuleringsmodell ferdig (Planlagt Medio Mai)
- [ ] **M5:** Endelig innlevering (1. juni)

---

# 8. Risiko

### Prosess for risikostyring
Risiko identifiseres løpende og dokumenteres i risikoregisteret.

### Risikoregister
| ID | Risiko | Sannsynlighet | Konsekvens | Tiltak |
|---|---|---|---|---|
| R1 | Manglende/mangelfulle data | Lav | Høy | Bruke estimater basert på fagekspertise. |
| R2 | For høy modellkompleksitet | Middels | Middels | Forenkle avgrensninger tidlig. |
| R3 | Tidsnød mot innlevering | Lav | Høy | Følge stram milepælsplan. |
| R4 | Avvik i validering (modell vs. virkelighet) | Middels | Høy | Sensitivitetsanalyse og sammenligning med manuelle logger/fagekspertise. |

---

# 9. Saker
| ID | Sak/Problemstilling | Status | Ansvarlig |
|---|---|---|---|
| [ ] S1 | Etablere stabil Python-omgivelse og installere SimPy | Åpen | Sandra |
| [x] S2 | Innhente og avklare format for flyprogrammer fra Avinor | Lukket | Sandra |
| [x] S3 | Kartlegge og lage oversikt over gater/remote stands (kompatibilitet og begrensninger) | Lukket | Sandra |

---

# 10. Interessenter
| Navn | Rolle | Interesse | Påvirkning |
|---|---|---|---|
| Sandra Christensen | Prosjektleder | Høy | Høy |
| Bård Inge Pettersen | Sponsor/Veileder | Høy | Høy |
| Per Kristian Rekdal | Sponsor/Veileder | Høy | Høy |
| Operativ leder Flesland | Kunde/Sluttbruker | Middels | Høy |

---

# 11. Ressurser

### Prosjektteam
- Sandra Christensen (Prosjektleder/Utvikler)

### Kritiske ressurser
- Tilgang til operative data fra Avinor.
- Veiledningstid fra faglærer.

---

# 12. Kommunikasjon

### Statusgjennomganger
Prosjektleder gjennomgår fremdrift mot plan annenhver uke. Tidspunkt tilpasses prosjektets faser og behovet for avklaringer.

### Veiledningsmøter
Gjennomføres fleksibelt etter avtale med veiledere (Bård Inge Pettersen og Per Kristian Rekdal). Møter kalles inn ved oppnådde milepæler eller ved behov for faglig støtte.

### Operativ dialog
Løpende kommunikasjon med kontaktpersoner hos Avinor for innhenting av data og operative avklaringer via e-post eller avtalte møter.

---

# 13. Kvalitet

### Fagfellevurderinger
- **Uformelle:** Gjennomgang av kode, simuleringslogikk og rapportutkast med medstudenter og veiledere for å sikre metodisk kvalitet.
- **Formelle:** Gjennomgang og tilbakemeldinger fra faglærere ved obligatoriske innleveringer og formelle veiledningsmøter.

### Brukerreviews
Planlagt systematisk gjennomgang av simuleringsmodellen og resultatene med operative kontakter ved Avinor. Hensikten er å validere at modellens antakelser og logikk (f.eks. gateallokering og bussing) stemmer overens med den faktiske operasjonen på Flesland.

---

# 14. Anskaffelser
Ingen eksterne anskaffelser er planlagt. Eksisterende programvare og lisenser benyttes.

---

# 15. Endringskontrollprosess
Eventuelle endringer i prosjektomfang eller milepæler skal dokumenteres og avklares med sponsor (faglærer) dersom de påvirker sluttresultatet vesentlig.

---

---

# 16. Vedlegg

### Vedlegg A – Kravliste
Dette vedlegget gir en oversikt over de spesifikke kravene prosjektet skal oppfylle.

| ID | Kravbeskrivelse | Type | Prioritet | Eier |
|---|---|---|---|---|
| K1 | Modellen skal kunne håndtere flyankomster med 15-30 min intervall. | Funksjonelt | Høy | Prosjektleder |
| K2 | Modellen skal skille mellom gate-tilkobling og remote stands. | Funksjonelt | Høy | Prosjektleder |
| K3 | Bussressurser (antall og kapasitet) skal modelleres som begrensning. | Ressurs | Høy | Prosjektleder |
| K4 | Antall tilgjengelige bussjåfører skal kunne varieres per skift. | Ressurs | Middels | Prosjektleder |
| K5 | Utdata skal inneholde gjennomsnittlig og maksimal ventetid før gate. | Analyse | Høy | Prosjektleder |
| K6 | Modellen skal støtte scenarioanalyse for endret trafikkvolum. | Analyse | Middels | Prosjektleder |
| K7 | Koden skal dokumenteres og være reproduserbar. | Teknisk | Middels | Prosjektleder |

### Vedlegg B – Risikoregister (detaljert)
Detaljert vurdering av identifiserte risikoer (Sannsynlighet og Konsekvens: 1-5).

| ID | Risiko | Sannsynlighet (1-5) | Konsekvens (1-5) | Risikoverdi (S x K) | Ansvarlig | Tiltak |
|---|---|---|---|---|---|---|
| R1 | Manglende operative logger | 2 | 5 | 10 | Sandra | Tidlig purring på data; bruk av manuelle logger som backup. |
| R2 | For kompleks simuleringslogikk | 3 | 3 | 9 | Sandra | Modulær oppbygging av koden; starte med en enkel grunnmodell. |
| R3 | Tidsnød mot 1. juni | 2 | 5 | 10 | Sandra | Ukentlig egenrevisjon av fremdrift mot milepæler. |
| R4 | Avvik i validering mot virkelighet | 3 | 4 | 12 | Sandra | Gjennomføre sensitivitetsanalyse og "sanity check" med Avinor. |

### Vedlegg C – WBS-ordliste
Beskrivelse av innholdet i de ulike arbeidspakkene.

| WBS ID | Arbeidspakke | Beskrivelse | Leveranse |
|---|---|---|---|
| 1.0 | Prosjektoppstart | Definere problemstilling, mål, avgrensninger og utarbeide prosjektstyringsplan. | Godkjent prosjektplan |
| 2.0 | Datainnsamling | Identifisere og innhente trafikkdata, gatekart og busslogger fra Avinor. | Strukturert datagrunnlag |
| 3.0 | Modellutvikling | Utvikle konseptuell logikk og programmere simuleringsmodellen i Python/SimPy. | Kildekode (v1.0) |
| 4.0 | Analyse (Baseline) | Kjøre simuleringer på dagens situasjon for å finne flaskehalser og kapasitetstak. | Analyseresultater |
| 5.0 | Scenarioanalyse | Teste effekten av å endre antall busser, sjåfører eller flyankomster. | Scenariorapport |
| 6.0 | Rapportering | Tolke funn, validere mot operative forhold og skrive ferdig LOG650-rapporten. | Sluttrapport |
