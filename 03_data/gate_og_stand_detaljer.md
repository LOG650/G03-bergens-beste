# Detaljert Oversikt over Gater og Stands - Bergen Lufthavn Flesland

Dette dokumentet fungerer som grunnlag for ressursallokering i simuleringsmodellen. Basert på kartet "Oversikt Flyoppstilling" har vi følgende inndeling:

## 1. Terminal 3 (Hovedsakelig Innland)
| Gate/Stand | Type | Sone | Beskrivelse / Bruk |
|:---|:---|:---|:---|
| 13 | Bussgate | Innland | Brukes til busstransport til remote stands eller fly i utlandssone. |
| 14 | Bussgate | Innland | Brukes til busstransport til remote stands eller fly i utlandssone. |
| 15 | Bro | Innland | |
| 16 | Bro | Innland | |
| 17 | Bro | Innland | |
| 18 | Bro | Innland | |
| 19 | Bro | Innland | |
| 20 | Bro | Innland | |

## 2. Terminal 2 (Internasjonal / Schengen / Flex)
| Gate/Stand | Type | Sone | Beskrivelse / Bruk |
|:---|:---|:---|:---|
| 23 | Bro | Non-Schengen | Nærmest passkontroll. |
| 24 | Bro | Schengen / Non-Schengen | Låses til Non-Schengen hvis 25+ er Non-Schengen. |
| 25 | Bro | Schengen / Non-Schengen | Låses til Non-Schengen hvis 26+ er Non-Schengen. |
| 26 | Bro | Schengen / Non-Schengen | |
| 27 | Bro | Schengen / Non-Schengen | |
| 28 | Bro | Innland / Schengen | Startpunkt for Innland-fleks. Låser 29-32 hvis Innland. |
| 29 | Bro | Innland / Schengen | Låser 30-32 hvis Innland. |
| 30 | Bussgate/Bro | Innland / Schengen | Kan brukes som både bro og bussgate (D/E). |
| 31 | Bro | Innland / Schengen | Låser 32 til Innland hvis denne brukes til Innland. |
| 32 | Bro | Innland / Schengen | Ytterste gate i piren. |
| 33 | Bussgate | Innland | C-utgang (Terminal 2). |
| 34 | Bussgate | Innland | C-utgang (Terminal 2). |


## 7. Logiske Regler for Sone-låsing (Simuleringslogikk)
*   **Passkontroll (Non-Schengen):** Ligger ved gate 23. Dersom en gate med høyere nummer (f.eks. 25) brukes til et fly fra utenfor Schengen, må alle gater med *lavere* numre (23, 24) også fungere som Non-Schengen soner.
*   **Sone-skille (Innland/Schengen):** Dersom en gate i serien 28-32 brukes til Innland (f.eks. gate 28), må alle gater med *høyere* numre i samme serie (29, 30, 31, 32) også låses til Innland for å opprettholde fysisk passasjerskille i terminalen.

## 3. Remote Stands - Nord
| Stand | Type | Bruk / Restriksjoner |
|:---|:---|:---|
| 1 | Remote | **Defekt.** Brukes ikke i normaldrift. |
| 2 | Remote | **Defekt.** Brukes ikke i normaldrift. |
| 3 | Remote | **Aktiv.** Vanlig remote stand for passasjerfly. |
| 4 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (opptil 186 pax/B737). |
| 5 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (opptil 186 pax/B737). |
| 6 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (registrert i busslogg). |
| 7 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (registrert i busslogg). |
| 8 | Remote | **Frakt / Crew.** Reservert DHL/Frakt-operasjoner. |
| 9 | Remote | Kan brukes samtidig med 11 (hvis 10 er ledig). |
| 10 | Remote | Kan bare brukes hvis 9 og 11 er ledige (overlapp). |
| 11 | Remote | Kan brukes samtidig med 9 (hvis 10 er ledig). |

## 8. Fysiske Begrensninger og Overlapp
*   **Remote Nord (9-10-11):** Stand 10 er en "sentrert" plass som fysisk blokkerer naboene 9 og 11. Modellen må velge mellom konfigurasjon (9+11) ELLER (10).
*   **Operativ prioritering:** Stand 1, 2 og 3 skal i utgangspunktet ikke telles som tilgjengelig kapasitet i normaldrift pga. tekniske/operative hindringer.

## 4. Remote Stands - Øst
| Stand | Type | Bruk / Restriksjoner |
|:---|:---|:---|
| 41 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (mye Widerøe). |
| 43 | Remote | **Aktiv.** Brukes til rute- og passasjerfly (mye Widerøe). |
| 46 | Remote | Spesialoppdrag / Ambulanse / Ikke-sikkerhetsklarert. |
| 47 | Remote | Spesialoppdrag / Ambulanse / Ikke-sikkerhetsklarert. |
| 48 | Remote | Spesialoppdrag / Ambulanse / Ikke-sikkerhetsklarert. |

## 5. Remote Stands - Sør (Ved hangarer)
| Stand | Type | Bruk / Restriksjoner |
|:---|:---|:---|
| 61-69 | Remote | Spesial / Langtidsparkering / Hangarbesøk. Ikke i bruk for pax. |
| DP 1-4 | De-ice | Oppstillingsplasser ved avisingsplattform. |

## 6. Spesialområder
| Område | Beskrivelse |
|:---|:---|
| GA 1-3 | General Aviation (Småfly) |
| GA F | Frakt / Cargo |
| H1-H9 | Hangarer |
