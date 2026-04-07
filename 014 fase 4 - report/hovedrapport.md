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
*Beskrivelse av økt trafikk på Flesland og behovet for effektiv gate-håndtering.*
### 1.2 Problemstilling
*Hvilken effekt har endringer i flyprogram eller ressursallokering (busser/gater) på passasjerflyten og forsinkelser?*
### 1.3 Forskningsspørsmål
*Spesifikke spørsmål som simuleringen skal besvare.*
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
### 3.2 Datainnsamling
*Beskrivelse av datasettene fra Avinor (Flyprogram juni 2026, busslogger).*
### 3.3 Simuleringsmodell (Modellbygging)
*Beskrivelse av logikken i `simulation.py`: agenter (fly), ressurser (gater, busser) og prosesser.*
### 3.4 Validering og Verifisering
*Hvordan vi sikrer at modellen reflekterer virkeligheten (sammenligning med busslogger).*

## 4. Resultater og Analyse
### 4.1 Deskriptiv statistikk av rådata
*Oversikt over trafikktopper og flytyper.*
### 4.2 Simuleringsresultater (Baseline)
*Hvordan systemet fungerer i dag.*
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
