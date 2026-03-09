# Proposal LOG650

**Gruppemedlemmer:**
Sandra Christensen

**Område:**
Kø-teori og kapasitetsplanlegging med fokus på ressursallokering og diskret hendelses-simulering av operativ kapasitet og ressursdimensjonering i peak-perioder.

**Bedrift (valgbart):**
Avinor – Bergen Lufthavn Flesland

**Problemstilling:**
Hvordan kan Avinor øke antall samtidige ankomster i peak-perioder ved optimal bruk av gater, remote stands og bussressurser, slik at ventetid og gate-relaterte forsinkelser reduseres uten ny infrastruktur?

Prosjektet skal analysere hvor mange samtidige ankomster systemet kan håndtere i peak-perioder før ventetid før gate overstiger et definert terskelnivå. Videre skal prosjektet undersøke hvordan optimal bruk av remote stands og bedre dimensjonering av bussressurser, inkludert antall innleide bussjåfører, kan bidra til å redusere forsinkelser og overflødig ressursbruk. Modellen skal også kunne brukes til å estimere hensiktsmessig nivå for innleie av bussjåfører basert på faktisk behov, slik at overflødige arbeidstimer reduseres.

**Data:**
*   Historiske ankomst- og avgangstider (15–30 minutters intervaller)
*   Faktiske on-block og off-block tider
*   Identifisering av peak-perioder
*   Antall passasjerer per fly (estimert eller faktisk)
*   Turnaround-tider per flytype inkludert variasjon
*   Gate- og standstruktur og kompatibilitetsregler (Schengen/non-Schengen, flytype)
*   Antall remote stands og tilgjengelighet i peak
*   Antall busser, kapasitet og syklustid
*   Antall bussjåfører tilgjengelig per periode
*   Faktisk brukstid og overflødige timer for innleide bussjåfører
*   Registrert ventetid før gate og gate-relaterte forsinkelser

**Beslutningsvariabler:**
*   Tildeling av fly til gate eller remote stand gitt kompatibilitetsregler
*   Prioriteringsregler ved samtidige ankomster
*   Dispatch og bruk av bussressurser
*   Antall bussjåfører tilgjengelig i peak-perioder
*   Dimensjonering av bussjåførkapasitet basert på trafikkprofil

**Målfunksjon:**
Hovedmålet er å maksimere antall samtidige ankomster som kan håndteres i peak-perioder uten at ventetid før gate overstiger et definert terskelnivå.

*   Redusere gate-relaterte forsinkelser
*   Sikre effektiv utnyttelse av bussressurser
*   Bidra til bedre beslutningsgrunnlag for planlegging av bussjåførressurser
*   Redusere overflødig kapasitet og ubrukte timer for innleide bussjåfører

**Avgrensninger:**
*   Ingen ny fysisk infrastruktur
*   Rutetider og trafikkstruktur antas gitt
*   Fokus på ankomstfasen i peak-perioder
*   Bemanning ved gater og øvrige terminalfunksjoner modelleres ikke eksplisitt
*   Buss og bussjåfører modelleres eksplisitt som begrensende ressurser
*   Analysen baseres på representative eller simulerte peak-perioder
*   Bidra til bedre beslutningsgrunnlag for planlegging av bussjåførressurser
