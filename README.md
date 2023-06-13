# Django-projekt
Projekt za predmet Izrada Web Aplikacija Django Framework-u

Zadatak za projekt
Izraditi sustav za upis studenata. Sustav ce se sastojati od tri uloge: student, profesor i
administrator.
Uloga administrator:
- autentikacija
- pregled i promjena liste predmeta
- dodavanje novog predmeta
- dodjeljivanje predmeta profesoru
- pregled liste studenata
- dodavanje i editiranje studenata
- izrada/promjena upisnog lista za bilo kojeg studenta
- pregled liste profesora
- dodavanje i editiranje profesora
- pregled popisa studenata za svaki pojedinacni predmet (na svaki predmet dodati link „vidi popis
studenata”)
- za administrator ulogu nije dozvoljeno koristiti Djangov admin sustav
Uloga profesor:
- autentikacija
- pregled liste predmeta prijavljenog profesora
- pregled popisa studenata na pojedinom kolegiju (kojem je prijavljeni profesor nositelj)
- mijenjanje statusa predmeta (po defaultu je samo upisan, a moze se promijeniti u „polozen” ili
„izgubio potpis”. Predmet se moze ispisati sve dok mu status nije promijenjen u polozen/izgubio
potpis)
- pregled studenata na svakom pojedinom predmetu prema sljedecim kriterijima:
1. studenti koji su izgubili potpis
2. studenti koji su dobili potpis, ali jos nisu polozili predmet
3. studenti koji su polozili predmet
Uloga student:
- autentikacija
- upis/ispis predmeta
Sve promjene u bazi vršiti preko POST zahtjeva. Obratiti pažnju na sigurnost aplikacije (kriptiranje
lozinki, SQL injection i XSS). Strukturu baze koja je na slici nize treba prilagoditi potrebama ovog
zadatka. Potrebno je dodati novu tablicu „uloge” u kojoj ce se
definirati uloge „admin”, „profesor” i „student” (u tablici korisnici izmijeniti stupac „uloga” iz
„enum” tipa podatka i napraviti relaciju na tablicu „uloge”). Tablica „korisnici” se razlikuje od Djangove tablice User. Potrebno ju je prilagoditi (vidi predavanja). Takodjer je potrebno prosiriti tablicu
„predmeti” sa stupcem koji definira nositelja kolegija. Taj stupac ce biti strani kljuc, a vezat ce se na
tablicu korisnici. Na aplikacijskoj razini je nuzno voditi racuna kako se za nositelja kolegija moze
postaviti samo korisnik koji ima ulogu profesor.
Na „upisnom listu“ svakog studenta se prikazuje lista neupisanih predmeta i lista
upisanih/položenih predmeta podijeljenih po semestrima (ovisno o statusu studenta). Izgled i
funkcionalnosti upisnog lista su iste za studente i administratora (osim izbornika u vrhu stranice).
Izbornik za studente će imati samo stavku „logout“ i prikazivati će se samo pripadajući upisni list.
Izbornik za administratora će imati „logout“, „predmeti“, „studenti“ i „profesori” preko kojih će se
pristupati ostalim prikazima. Profesor u izborniku na vrhu stranice ima stavke „predmeti” (prikaz
predmeta kojima je on nositelj) i stavku „logout”. Odabirom svakog pojedinog predmeta ima uvid u
studente koji su ih upisali i njihove statuse. Kod je potrebno izraditi u radnom okviru Django.
Realizirati i organizirati kôd prema MVC (MVT) arhitekturi. Obavezno je imati strukturu koju je
relativno lako proširiti sa manjim dodatnim funkcionalnostima (npr. dodati i prikazati zbroj upisanih
ECTS bodova).
Funkcionalnosti i sigurnost su glavne stavke, ali u ocjenu će ulaziti i upotrebljivost sučelja i
organizacija kôda.
Primjer izgleda sucelja:

Pravila:
Obrana projekta se održava u sklopu ispita. Sastojati će se od pismenog ispita, u vidu jednog ili više
zadataka (npr. dodati linkove koji vode na opise predmeta uz prikaz liste predmeta i sl.) kojeg je
potrebno odraditi u zadanom vremenskom roku. Nakon pismenog ispita organizirati će se usmeni
ispit. Na usmenom ispitu će svaki student prezentirati svoj projekt, te će trebati odgovarati na pitanja
vezana uz kôd u projektu. Primjerice - pokazati kroz kôd kako se upiše novi predmet. Projekt je
potrebno predati najkasnije tri radna dana prije planiranog ispitnog roka (ako je ispit u utorakprojekt je potrebno predati najkasnije do cetvrtka do 23.59 sati ili ako je ispit u petak projekt je
potrebno predati najkasnije do utorka do 23.59 sati). Zakašnjeli projekti se automatizmom prebacuju
na idući ispitni rok.
